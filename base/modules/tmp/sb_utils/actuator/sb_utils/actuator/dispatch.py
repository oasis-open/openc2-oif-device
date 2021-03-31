"""
Multiple dispatch on namespace
"""
from functools import partial
from inspect import isfunction
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Union
)

from sb_utils import QueryDict


DispatchTransform = Callable[[tuple, dict], Tuple[Union[tuple, None], dict]]


class Dispatch:
    _dispatch_transform: Callable[[tuple, dict], Tuple[Union[tuple, None], dict]]
    _func_kwargs: Dict[str, Any]
    _namespace: str
    _registered: QueryDict

    def __init__(self, namespace="Dispatch", dispatch_transform: DispatchTransform = None, **kwargs) -> None:
        """
        Initialize a Dispatch object
        :param namespace: Namespace of the dispatch - default 'Dispatch'
        :param dispatch_transform: function to call prior to a registered function - fun(tuple, dict) -> Tuple[Union[None, tuple], dict]
        :param kwargs: kwargs to pass to the function being called
        """
        self._namespace = namespace
        self._dispatch_transform = dispatch_transform
        self._func_kwargs = kwargs
        self._registered = QueryDict(
            default=lambda *a, **k: AttributeError("Default function not set")
        )

    @property
    def namespace(self) -> str:
        """
        Namespace of the dispatch
        :return: dispatch namespace
        """
        return self._namespace

    @property
    def registered(self) -> List[str]:
        """
        Composite keys of the registered function of the dispatch
        separated by a '.' -> 'Namespace.Key'
        :return: composite keys
        """
        return self._registered.compositeKeys()

    # pylint: disable=keyword-arg-before-vararg
    def dispatch(self, key: str = None, *args, **kwargs) -> dict:
        """
        Dispatch function based on the given key with the args and kwargs
        :param key: key/namespace of the function to call
        :param args: args to pass to the function
        :param kwargs: key word args to pass to the function
        :return: function results - dict
        """
        fun_kwargs = self._func_kwargs.copy()
        fun_kwargs.update(kwargs)

        if fun_trans := self._dispatch_transform:
            args, fun_kwargs = fun_trans(*args, **fun_kwargs)

        fun = self._dispatch(key, init=True)
        return fun(*args, **fun_kwargs) if isinstance(args, tuple) else kwargs

    # pylint: disable=keyword-arg-before-vararg
    def register(self, fun: Callable = None, key: str = None) -> Callable:
        """
        Register a function
        usable as a wrapper or standard function call
        :param fun: function to register
        :param key: name to register as, default function name
        """
        if fun is None and key:
            return partial(self.register, key=key)

        key = key or fun.__name__
        self._registered[key] = fun
        return fun

    def register_dispatch(self, dispatch: 'Dispatch') -> None:
        """
        Register another Dispatch as a key
        :param dispatch: Dispatch instance to register
        """
        if dispatch.namespace:
            if dispatch.namespace in self._registered:
                raise NameError(f"Cannot register a namespace twice, {dispatch.namespace} already exists")
            self._registered[dispatch.namespace] = dispatch._registered
        else:
            raise AttributeError("Cannot register a dispatch without a namespace")

    # Helper Functions
    def _dispatch(self, key="", rem_key: Tuple[str, ...] = (), init=False) -> Callable[[tuple, dict], dict]:
        """
        dispatch function helper, get nested function if available
        :param key: key/namespace of the function to call
        :param rem_key: remaining portion of the key
        :param init: initial call of function
        :return: registered function
        """
        if len(rem_key) == 0 and init:
            keys = key.split(".")
            key = keys[0]
            rem_key = tuple(keys[1:])

        if val := self._registered.get(key, None):
            if isfunction(val) and not init:
                return val
            return self._dispatch(".".join([key, rem_key[0]]), rem_key=() if len(rem_key) == 0 else rem_key[1:])
        return self._registered.get(".".join([*key.split(".")[:-1], "default"]), self._registered["default"])
