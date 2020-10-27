import copy

from typing import (
    Any,
    List,
    Sequence
)

from .general import safe_cast


# Dictionary Methods
# ...


# Dictionary Classes
class ObjectDict(dict):
    """
    Dictionary that acts like a object
    d = ObjectDict()

    d['key'] = 'value'
        SAME AS
    d.key = 'value'
    """

    def __getattr__(self, key: Any) -> Any:
        """
        Get an key as if an attribute - ObjectDict.key - SAME AS - ObjectDict['key']
        :param key: key to get value of
        :return: value of given key
        """
        if key in self:
            return self[key]
        raise AttributeError(f"No such attribute {key}")

    def __setattr__(self, key: Any, val: Any) -> None:
        """
        Set an key as if an attribute - d.key = 'value' - SAME AS - d['key'] = 'value'
        :param key: key to create/override
        :param val: value to set
        :return: None
        """
        self[key] = self.__class__(val) if isinstance(val, dict) else val

    def __delattr__(self, key: Any) -> None:
        """
        Remove a key as if an attribute - del d.key - SAME AS - del d['key']
        :param key: key to remove/delete
        :return: None
        """
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"No such attribute: {key}")


class FrozenDict(ObjectDict):
    """
    Immutable/Frozen dictionary
    """
    _hash: hash

    def __init__(self, seq: Sequence = None, **kwargs) -> None:
        """
        Initialize an QueryDict
        :param seq: initial Sequence data
        :param kwargs: key/value parameters
        """
        if seq:
            ObjectDict.__init__(self, seq, **kwargs)
        else:
            ObjectDict.__init__(self, **kwargs)

        for k, v in self.items():
            if isinstance(v, dict) and not isinstance(v, self.__class__):
                ObjectDict.__setitem__(self, k, FrozenDict(v))
            elif isinstance(v, (list, tuple)):
                ObjectDict.__setitem__(self, k, tuple(FrozenDict(i) if isinstance(i, dict) else i for i in v))

    def __hash__(self) -> hash:
        """
        Create a hash for the FrozenDict
        :return: object hash
        """
        if self._hash is None:
            self._hash = hash(tuple(sorted(self.items())))
        return self._hash

    def _immutable(self, *args, **kwargs) -> None:
        """
        Raise an error for an attempt to alter the FrozenDict
        :param args: positional args
        :param kwargs: key/value args
        :return: None
        :raise TypeError
        """
        raise TypeError('cannot change object - object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    pop = _immutable
    popitem = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable


class QueryDict(ObjectDict):
    """
    Nested Key traversal dictionary
    d = QueryDict()

    d['192']['168']['1']['100'] = 'test.domain.local'
        SAME AS
    d['192.168.1.100'] = 'test.domain.local'
    """
    separator: str = "."

    def __init__(self, seq: Sequence = None, **kwargs) -> None:
        """
        Initialize an QueryDict
        :param seq: initial Sequence data
        :param kwargs: key/value parameters
        """
        if seq:
            ObjectDict.__init__(self, seq, **kwargs)
        else:
            ObjectDict.__init__(self, **kwargs)

        for k, v in self.items():
            if isinstance(v, dict) and not isinstance(v, self.__class__):
                ObjectDict.__setitem__(self, k, QueryDict(v))
            elif isinstance(v, (list, tuple)):
                ObjectDict.__setitem__(self, k, type(v)(QueryDict(i) if isinstance(i, dict) else i for i in v))

    # Override Functions
    def get(self, path: str, default: Any = None, sep: str = None) -> Any:
        """
        Get a key/path from the QueryDict
        :param path: key(s) to get the value of separated by the separator character
        :param default: default value if the pey/path is not found
        :param sep: separator character to use, default - '.'
        :return: value of key/path or default
        """
        sep = sep if sep else self.separator
        path = self._pathSplit(str(path), sep)

        if any(k.startswith(sep.join(path)) for k in self.compositeKeys()):
            rtn = self
            for key in path:
                if isinstance(rtn, ObjectDict):
                    rtn = ObjectDict.__getitem__(rtn, key)
                elif isinstance(rtn, (list, tuple)) and len(rtn) > safe_cast(key, int, key):
                    rtn = rtn[safe_cast(key, int, key)]
                else:
                    raise AttributeError(f"Unknown type {type(rtn)}, cannot get value")
            return rtn
        return default

    def set(self, path: str, val: Any, sep: str = None) -> None:
        """
        Set a key/path in the QueryDict object
        :param path: key/path to set
        :param val: value to set
        :param sep: separator character to use, default - '.'
        :return: None
        """
        sep = sep if sep else self.separator
        keys = self._pathSplit(str(path), sep)

        if isinstance(val, dict):
            val = QueryDict(val)
        elif isinstance(val, (list, tuple)):
            val = type(val)(QueryDict(i) if isinstance(i, dict) else i for i in val)

        obj = self
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

    def delete(self, path: str, sep: str = None) -> None:
        """
        Delete a key/path in the QueryDict object
        :param path: key/path to delete
        :param sep: separator character to use, default - '.'
        :return: None
        """
        sep = sep if sep else self.separator
        path = self._pathSplit(path, sep)

        if any(k.startswith(sep.join(path)) for k in self.compositeKeys()):
            ref = self
            for idx, key in enumerate(path):
                key = safe_cast(key, int, key)
                end = len(path) == idx + 1

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
                        raise KeyError(f"{sep.join(path[:idx])} does not exist")

                else:
                    print(f"Other - {type(ref)}")

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
        return QueryDict(copy.deepcopy(dict(self), memo))

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
        sep = sep if sep else self.separator
        return self._compositeKeys(self, sep)

    # Helper Functions
    def _compositeKeys(self, obj: Any, sep: str = None) -> List[str]:
        """
        Determine the composite keys of the given object
        :param obj: object to get the composite keys
        :param sep: path separator character
        :return: list of keys
        """
        sep = sep if sep else self.separator
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

    def _pathSplit(self, path: str, sep: str = None) -> List[str]:
        """
        Split the path based on the separator character
        :param path: path to split
        :param sep: separator character
        :return: list of separated keys
        """
        sep = sep if sep else self.separator
        return list(filter(None, path.split(sep)))
