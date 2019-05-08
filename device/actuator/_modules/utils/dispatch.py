# Multiple dispatch on namespace

from typing import Any, Callable, List


class MultiKeyDict(dict):
    def __init__(self, sep: str = '.', *args, **kwargs) -> None:
        super(MultiKeyDict, self).__init__(*args, **kwargs)
        self._sep = sep
        for k, v in dict(self).items():
            if self._sep in k:
                dict.__delitem__(self, k)
                keys = list(filter(None, k.split(self._sep)))
                dict.setdefault(self, keys[0], MultiKeyDict(sep=self._sep))
                self[keys[0]][self._sep.join(keys[1:])] = v

    def __setitem__(self, key: str, val: Any) -> None:
        keys = list(filter(None, key.split(self._sep)))
        if len(keys) == 1:
            dict.__setitem__(self, key, val)
        else:
            self[keys[0]] = MultiKeyDict(
                sep=self._sep,
                **{
                    **dict.get(self, keys[0], {}),
                    self._sep.join(keys[1:]): val,
                }
            )

    def __getitem__(self, key: str) -> Any:
        keys = list(filter(None, key.split(self._sep)))
        if len(keys) == 1:
            return dict.__getitem__(self, key)
        else:
            rtn = self
            for key in keys:
                rtn = dict.get(rtn, key, None)
            return rtn

    def __delitem__(self, key: str) -> None:
        keys = list(filter(None, key.split(self._sep)))
        if len(keys) == 1:
            dict.__delitem__(self, key)
        else:
            k = dict.get(self, keys[0], None)
            if k:
                k.__delitem__(self._sep.join(keys[1:]))

    def __contains__(self, item) -> bool:
        keys = list(filter(None, item.split(self._sep)))
        return item in self._compositKeys(self) if len(keys) > 1 else dict.get(self, item, None) is not None

    def get(self, key: str, default: Any = None) -> Any:
        return self[key] if key in self else default

    def compositKeys(self) -> List[str]:
        return self._compositKeys(self)

    # helper functions
    def _compositKeys(self, obj: dict) -> List[str]:
        if isinstance(obj, self.__class__):
            tmp = []
            for key, val in obj.items():
                val_keys = self._compositKeys(val) 
                if len(val_keys) > 0:
                    tmp.extend([f'{key}{self._sep}{k}' for k in val_keys])
                else:
                    tmp.append(key)
            return tmp
        else:
            return []


class Dispatch(object):
    _namespace: str
    _func_kwargs = dict
    _functions: MultiKeyDict

    def __init__(self, namespace: str = None, **kwargs):
        self._namespace = namespace
        self._func_kwargs = kwargs
        self._functions = MultiKeyDict(
            default=lambda *args, **kwargs: AttributeError("Default function not set")
        )

    @property
    def namespace(self):
        return self._namespace

    @property
    def registered(self):
        return self._functions

    # Dispatch action
    def dispatch(self, key: str = None, *args, **kwargs):
        fun = self._functions.get(key, self._functions["default"])
        fun_kwargs = dict(self._func_kwargs)
        fun_kwargs.update(kwargs)
        return fun(*args, **fun_kwargs)

    # Register a function, wrapper or standard function call
    def register(self, fun: Callable, key: str = None):
        key = key if key else fun.__name__
        self._functions[key] = fun

    # register another Dispatch as a namespace
    def register_dispatch(self, dispatch: object = None):
        if dispatch.namespace:
            self._functions[dispatch.namespace] = dispatch.registered
        else:
            raise AttributeError("Cannot register a dispatch without a namespace")
