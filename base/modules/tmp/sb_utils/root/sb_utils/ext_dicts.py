"""
Extended Dict Utils
"""
import copy

from typing import Any, List, MutableMapping, Type
from .general import safe_cast
__all__ = ["ObjectDict", "FrozenDict", "QueryDict"]


# Dictionary Helpers
def pdoc_wrapped_fix(wraps: Type = object):
    # TODO: fix extended dics so this wrapper is not necessary
    def inner(cls: Type) -> Type:
        if wraps != object:
            attrs = {*dir(cls)} - {*dir(wraps)}
            cls.__wrapped__ = type(cls.__name__, (wraps, ), {k: getattr(cls, k) for k in attrs if not k.startswith("_")})
        return cls
    return inner


def immutable(*args, **kwargs) -> None:
    """
    Raise an error for an attempt to alter the FrozenDict
    :param args: positional args
    :param kwargs: key/value args
    :raise TypeError
    """
    raise TypeError('cannot change object - object is immutable')


# Dictionary Classes
@pdoc_wrapped_fix(dict)
class ObjectDict(dict):
    """
    Dictionary that acts like an object
    ```python
    d = ObjectDict()

    d['key'] = 'value'
        SAME AS
    d.key = 'value'
    ```
    """
    def __init__(self, seq: MutableMapping = None, **kwargs):
        """
        Initialize an ObjectDict
        :param args: positional parameters
        :param kwargs: key/value parameters
        """
        cls = self.__class__
        data = dict(seq or {}, **kwargs)
        for k, v in data.items():
            if isinstance(v, dict) and not isinstance(v, cls):
                data[k] = cls(v)
            elif isinstance(v, (list, tuple)):
                data[k] = tuple(cls(i) if isinstance(i, dict) else i for i in v)
        super().__init__(data)

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict):
            value = self.__class__(value)  # if len(value.keys()) > 0 else self.__class__()
        super().__setitem__(key, value)

    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__
    __delattr__ = dict.__delitem__

    def __copy__(self):
        cls = self.__class__
        return cls(copy.copy(dict(self)))

    def __deepcopy__(self, memo):
        cls = self.__class__
        return cls(copy.deepcopy(dict(self)))

    def update(self, seq: MutableMapping = None, **kwargs) -> None:
        """Updates the dictionary with the specified key-value pairs"""
        data = dict(seq or {}, **kwargs)
        for k, v in data.items():
            if isinstance(v, dict) and not isinstance(v, self.__class__):
                data[k] = self.__class__(v)
            elif isinstance(v, (list, tuple)):
                data[k] = tuple(self.__class__(i) if isinstance(i, dict) else i for i in v)
        super().update(data)


@pdoc_wrapped_fix(dict)
class FrozenDict(ObjectDict):
    """
    Immutable/Frozen dictionary
    The API is the same as `dict`, without methods that can change the
    immutability. In addition, it supports __hash__().
    """
    __slots__ = ("_hash", )
    _hash: hash

    def __hash__(self) -> hash:
        """
        Calculates the hash if all values are hashable
        :raise TypeError: if a value is not hashable
        :return: object hash
        """
        if self._hash is None:
            self._hash = hash(frozenset(self.items()))
        return self._hash

    __setattr__ = immutable
    __setitem__ = immutable
    __delattr__ = immutable
    __delitem__ = immutable
    clear = immutable
    pop = immutable
    popitem = immutable
    update = immutable
    setdefault = immutable

    # Custom functions
    def unfreeze(self) -> dict:
        """
        Convert the 'FrozenDict' to a standard dict with editable values
        :return: standard dict
        """
        rtn = {}
        for k, v in self.items():
            rtn[k] = self._unfreeze(v)

        return rtn

    # Helper functions
    def _unfreeze(self, obj: Any) -> Any:
        if isinstance(obj, self.__class__):
            return obj.unfreeze()
        if isinstance(obj, tuple):
            return [self._unfreeze(i) for i in obj]
        return obj


@pdoc_wrapped_fix(dict)
class QueryDict(ObjectDict):
    """
    Nested Key traversal dictionary
    d = QueryDict()

    d['192']['168']['1']['100'] = 'test.domain.local'
        SAME AS
    d['192.168.1.100'] = 'test.domain.local'
    """
    separator: str = "."

    # Override Functions
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a key/path from the QueryDict
        :param path: key(s) to get the value of separated by the separator character
        :param default: default value if the key/path is not found
        :return: value of key/path or default
        """
        if self.separator in path:
            keys = self._pathSplit(str(path))
            if any(k.startswith(path) for k in self.compositeKeys()):
                rtn = self
                for key in keys:
                    if isinstance(rtn, ObjectDict):
                        rtn = ObjectDict.__getitem__(rtn, key)
                    elif isinstance(rtn, (list, tuple)) and len(rtn) > safe_cast(key, int, key):
                        rtn = rtn[safe_cast(key, int, key)]
                    else:
                        raise AttributeError(f"Unknown type {type(rtn)}, cannot get value")
                return rtn
        elif path in self:
            return ObjectDict.__getitem__(self, path)

        return default

    def set(self, path: str, val: Any) -> None:
        """
        Set a key/path in the QueryDict object
        :param path: key/path to set
        :param val: value to set
        :return: None
        """
        if isinstance(val, dict):
            val = QueryDict(val)
        elif isinstance(val, (list, tuple)):
            val = type(val)(QueryDict(i) if isinstance(i, dict) else i for i in val)

        obj = self
        keys = self._pathSplit(str(path))
        for idx, key in enumerate(keys):
            key = safe_cast(key, int, key)
            next_key = safe_cast(keys[idx + 1], int, keys[idx + 1]) if len(keys) > idx + 1 else ""
            end = len(keys) == idx + 1

            if end:
                if isinstance(obj, list) and isinstance(key, int):
                    if len(obj) <= key:
                        obj.append(val)
                    else:
                        obj[key] = val
                elif isinstance(obj, ObjectDict):
                    ObjectDict.__setitem__(obj, key, val)
                else:
                    print(f"Other - {type(obj)}")
            elif key in obj:
                obj = obj[key]
            elif isinstance(obj, list) and isinstance(key, int):
                if len(obj) <= key:
                    obj.append([] if isinstance(next_key, int) else ObjectDict())
                    obj = obj[-1]
                else:
                    obj = obj[key]
            elif isinstance(obj, ObjectDict):
                obj = obj.setdefault(key, [] if isinstance(next_key, int) else ObjectDict())
            else:
                obj = obj.setdefault(key, [] if isinstance(next_key, int) else ObjectDict())

    def delete(self, path: str) -> None:
        """
        Delete a key/path in the QueryDict object
        :param path: key/path to delete
        :return: None
        """
        if any(k.startswith(path) for k in self.compositeKeys()):
            ref = self
            keys = self._pathSplit(path)
            for idx, key in enumerate(keys):
                key = safe_cast(key, int, key)
                end = len(keys) == idx + 1

                if end:
                    if isinstance(ref, list) and isinstance(key, int):
                        if len(ref) > key:
                            ref.remove(ref[key])
                    elif isinstance(ref, ObjectDict):
                        ObjectDict.__delitem__(ref, key)
                    else:
                        print(f"Other - {type(ref)}")
                elif key in ref:
                    ref = ref[key]
                elif isinstance(ref, list) and isinstance(key, int):
                    if len(ref) > key:
                        ref = ref[key]
                    else:
                        raise KeyError(f"{self.separator.join(keys[:idx])} does not exist")
                else:
                    print(f"Other - {type(ref)}")

    def setdefault(self, path: str, default: Any) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.
        Return the value for key if key is in the dictionary, else default.
        """
        if path not in self.compositeKeys():
            self.set(path, default)
        return self.get(path)

    def __contains__(self, path: str) -> bool:
        """
        Verify if a key is in the MultiKeyDict - 'key0' in d and 'key1' in d['key0'] - SAME AS - 'key0.key1' in d
        :param path: path to verify if contained
        :return: if MultiKeyDict contains the given key
        """
        keys = self._pathSplit(path)
        return path in self._compositeKeys(self) if len(keys) > 1 else ObjectDict.__contains__(self, path)

    def __deepcopy__(self, memo):
        """
        Copy the QueryDict without referencing the original data
        :param memo: ...
        :return: copy of QueryDict
        """
        return QueryDict(copy.deepcopy(dict(self)))

    __getattr__ = get
    __getitem__ = get
    __setattr__ = set
    __setitem__ = set
    __delattr__ = delete
    __delitem__ = delete

    # Custom Functions
    def compositeKeys(self, sep: str = None) -> List[str]:
        """
        Compiled list of keys
        :param sep: key separator character
        :return: list of composite keys
        """
        sep = sep or self.separator
        return self._compositeKeys(self, sep)

    def setSeperator(self, value: str) -> None:
        """
        Set the seperator character for the 'QueryDict'
        :param value: single character to use as the seperator
        """
        self.separator = value

    # Helper Functions
    def _compositeKeys(self, obj: Any, sep: str = None) -> List[str]:
        """
        Determine the composite keys of the given object
        :param obj: object to get the composite keys
        :param sep: path separator character
        :return: list of keys
        """
        sep = sep or self.separator
        rtn = []
        key_vals = {}
        if isinstance(obj, self.__class__):
            key_vals = obj.items()
        elif isinstance(obj, (list, tuple)):
            key_vals = enumerate(obj)

        for key, val in key_vals:
            val_keys = self._compositeKeys(val, sep)
            rtn.extend([f"{key}{sep}{k}" for k in val_keys] if len(val_keys) > 0 else [key])

        return rtn

    def _pathSplit(self, path: str) -> List[str]:
        """
        Split the path based on the separator character
        :param path: path to split
        :param sep: separator character
        :return: list of separated keys
        """
        return list(filter(None, path.split(self.separator)))
