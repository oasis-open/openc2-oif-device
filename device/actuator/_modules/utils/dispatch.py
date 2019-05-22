# Multiple dispatch on namespace

from inspect import isfunction
from typing import Callable, Tuple

from .general import MultiKeyDict


class Dispatch(object):
    _namespace: str
    _func_kwargs = dict
    _functions: MultiKeyDict

    def __init__(self, namespace: str = None, dispatch_transform: Callable[[tuple, dict], Tuple[tuple, dict]] = None, **kwargs):
        self._namespace = namespace
        self._dispatch_transform = dispatch_transform
        self._func_kwargs = kwargs
        self._functions = MultiKeyDict(
            default=lambda *args, **kwargs: AttributeError("Default function not set")
        )

    @property
    def namespace(self):
        return self._namespace

    @property
    def registered(self):
        return self._functions.compositKeys()

    # Dispatch action
    def dispatch(self, key: str = None, *args, **kwargs):
        fun = self._dispatch(key, init=True)
        fun_kwargs = dict(self._func_kwargs)
        fun_kwargs.update(kwargs)

        if self._dispatch_transform:
            args, fun_kwargs = self._dispatch_transform(*args, **fun_kwargs)

        return fun(*args, **fun_kwargs) if isinstance(args, tuple) else kwargs

    # Register a function, wrapper or standard function call
    def register(self, fun: Callable, key: str = None):
        key = key if key else fun.__name__
        self._functions[key] = fun

    # register another Dispatch as a namespace
    def register_dispatch(self, dispatch: object = None):
        if dispatch.namespace:
            self._functions[dispatch.namespace] = dispatch._functions
        else:
            raise AttributeError("Cannot register a dispatch without a namespace")

    # Helper Functions
    def _dispatch(self, key: str = "", rem_key: tuple = (), init: bool = False):
        if len(rem_key) == 0 and init:
            keys = key.split(".")
            key = keys[0]
            rem_key = tuple(keys[1:])

        val = self._functions.get(key, None)
        if val:
            if isfunction(val) and not init:
                return val
            else:
                return self._dispatch(".".join([key, rem_key[0]]), rem_key=() if len(rem_key) == 0 else rem_key[1:])
        else:
            return self._functions.get(".".join([*key.split(".")[:-1], "default"]), self._functions["default"])
