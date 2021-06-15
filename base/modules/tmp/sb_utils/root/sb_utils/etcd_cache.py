"""
Local Cache for ETCd values
"""
import etcd

from threading import Event, Thread
from time import sleep
from typing import Callable, List, Tuple, Union
from .general import isFunction
from .ext_dicts import FrozenDict, QueryDict


# Type Hinting
Callback = Callable[[FrozenDict], None]
Callbacks = Union[
    List[Callback],
    Tuple[Callback, ...]
]


class ReusableThread(Thread):
    """
    Base: https://www.codeproject.com/Tips/1271787/Python-Reusable-Thread-Class
    This class provides code for a restartale / reusable thread

    join() will only wait for one (target)functioncall to finish
    finish() will finish the whole thread (after that, it's not restartable anymore)
    """

    def __init__(self, target: Callable, args: tuple = None, kwargs: dict = None):
        self._startSignal = Event()
        self._oneRunFinished = Event()
        self._finishIndicator = False
        self._callable = target
        self._callableArgs = args or ()
        self._callableKwargs = kwargs or {}
        Thread.__init__(self)

    def restart(self) -> None:
        """
        make sure to always call join() before restarting
        """
        self._startSignal.set()

    def run(self) -> None:
        """
        This class will reprocess the object "processObject" forever.
        Through the change of data inside processObject and start signals
        we can reuse the thread's resources
        """
        self.restart()
        while True:
            # wait until we should process
            self._startSignal.wait()
            self._startSignal.clear()
            if self._finishIndicator:  # check, if we want to stop
                self._oneRunFinished.set()
                return

            # call the threaded function
            self._callable(*self._callableArgs, **self._callableKwargs)
            # notify about the run's end
            self._oneRunFinished.set()

    def join(self, timeout: float = None) -> None:
        """
        This join will only wait for one single run (target functioncall) to be finished
        """
        self._oneRunFinished.wait(timeout)
        self._oneRunFinished.clear()
        self.restart()

    def finish(self) -> None:
        self._finishIndicator = True
        self.restart()
        self.join(5)


class EtcdCache:
    _callbacks: List[Callback]
    _data: QueryDict
    _etcd_client: etcd.Client
    _etcd_updater: ReusableThread
    _root: str
    _timeout: int

    def __init__(self, host: str, port: int, base: str, timeout: int = 60, callbacks: Callbacks = None):
        super().__init__()
        self._callbacks = []
        if isinstance(callbacks, (list, tuple)):
            self._callbacks.extend([f for f in callbacks if isFunction(f)])

        self._data = QueryDict()
        self._etcd_client = etcd.Client(
            host=host,
            port=port
        )
        self._root = base if base.endswith('/') else f'{base}/'
        self._timeout = timeout
        self._initial()
        self._etcd_updater = ReusableThread(target=self._update, kwargs={'wait': True})
        self._etcd_updater.setDaemon(True)
        self._etcd_updater.start()

    @property
    def cache(self) -> FrozenDict:
        return FrozenDict(self._data)

    def shutdown(self) -> None:
        self._etcd_updater.join(5)
        self._etcd_updater.finish()

    # Helper Methods
    def _initial(self, base: str = None) -> None:
        """
        Get ETCD initial values
        """
        root = base or self._root
        try:
            for k in self._etcd_client.read(root, recursive=True, sorted=True).children:
                key = k.key.replace(self._root, '').replace('/', '.')
                self._data[key] = k.value
        except (etcd.EtcdKeyNotFound, etcd.EtcdWatchTimedOut):
            pass

    def _update(self, wait: bool = False, base: str = None) -> None:
        """
        Get ETCD value updates
        """
        root = base or self._root
        kwargs = dict(wait=True, timeout=self._timeout) if wait else {}
        update = False

        try:
            for k in self._etcd_client.read(root, recursive=True, sorted=True, **kwargs).children:
                update = True
                key = k.key.replace(self._root, '').replace('/', '.')
                t_id = key.split('.')[0]
                if t_id not in self._data:
                    sleep(0.5)
                    self._initial(base=f'{root}{t_id}')
                else:
                    if k.value is None:
                        del self._data[key]
                    else:
                        self._data[key] = k.value
            update = True
        except (etcd.EtcdKeyNotFound, etcd.EtcdWatchTimedOut):
            pass

        if update:
            for func in self._callbacks:
                func(self.cache)

        if self._etcd_updater.is_alive():
            self._etcd_updater.join(5)
            self._etcd_updater.restart()
        else:
            self._etcd_updater.start()
