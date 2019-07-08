from typing import Any, List


class ObjectDict(dict):
    """
    Dictionary that acts like a object
    d = ObjectDict()

    d['key'] = 'value'
        SAME AS
    d.key = 'value'
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize an ObjectDict
        :param args: positional parameters
        :param kwargs: key/value parameters
        """
        self._hash = None
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key: str) -> Any:
        """
        Get an key as if an attribute - ObjectDict.key - SAME AS - ObjectDict['key']
        :param key: key to get value of
        :return: value of given key
        """
        if key in self:
            return self[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key: str, val: Any) -> None:
        """
        Set an key as if an attribute - d.key = 'value' - SAME AS - d['key'] = 'value'
        :param key: key to create/override
        :param val: value to set
        :return: None
        """
        dict.__setitem__(self, key, val)


class FrozenDict(ObjectDict):
    """
    Immutable dictionary
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a FrozenDict
        :param args: positional parameters
        :param kwargs: key/value parameters
        """
        super(FrozenDict, self).__init__(*args, **kwargs)

    def __hash__(self) -> int:
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


class MultiKeyDict(ObjectDict):
    """
    Multi Key traversal dictionary
    d = MultiKeyDict()

    d['192']['168']['1']['100'] = 'test.domain.local'
        SAME AS
    d['192.168.1.100'] = 'test.domain.local'
    """

    def __init__(self, sep: str = '.', *args, **kwargs) -> None:
        """
        Initialize an MultiKeyDict
        :param sep: key delimiter
        :param args: positional parameters
        :param kwargs: key/value parameters
        """
        if isinstance(sep, (dict, list, tuple)):
            self._sep = '.'
            if isinstance(sep, dict):
                kwargs.update(sep)
            else:
                for i, itm in enumerate(sep):
                    if len(itm) != 2:
                        raise ValueError(f"cannot initialize MultiKeyDict with item #{i}, expected length 2 but given length {len(itm)}")
                    kwargs[itm[0]] = itm[1]
        else:
            self._sep = sep

        super(MultiKeyDict, self).__init__(*args, **kwargs)

        for k, v in dict(self).items():
            if self._sep in k:
                dict.__delitem__(self, k)
                keys = self._keySplit(k)
                dict.setdefault(self, keys[0], MultiKeyDict(sep=self._sep))[self._sep.join(keys[1:])] = v

    def __setitem__(self, key: str, val: Any) -> None:
        """
        Set a key as if an attribute - d.key0.key1 = 'value'
        :param key: key to create/override
        :param val: value to set
        :return: None
        """
        keys = self._keySplit(key)
        if len(keys) == 1:
            super().__setitem__(key, val)
        else:
            self[keys[0]] = MultiKeyDict(
                sep=self._sep,
                **{
                    **dict.get(self, keys[0], {}),
                    self._sep.join(keys[1:]): val,
                }
            )

    def __getitem__(self, key: str) -> Any:
        """
        Get a key - del d['key0']['key1'] - SAME AS - del d['key0.key1']
        :param key: key to get value of
        :return: value of given key
        """
        keys = self._keySplit(key)
        if len(keys) == 1:
            return dict.__getitem__(self, key)
        else:
            rtn = self
            for key in keys:
                rtn = dict.get(rtn, key, None)
            return rtn

    def __delitem__(self, key: str) -> None:
        """
        Delete a key - val = d['key0']['key1'] - SAME AS - val = d['key0.key1']
        :param key: key to get value of
        :return: value of given key
        """
        keys = self._keySplit(key)
        if len(keys) == 1:
            dict.__delitem__(self, key)
        else:
            k = dict.get(self, keys[0], None)
            if k:
                k.__delitem__(self._sep.join(keys[1:]))

    def __contains__(self, key) -> bool:
        """
        Verify if a key is in the MultiKeyDict - 'key0' in d and 'key1' in d['key0'] - SAME AS - 'key0.key1' in d
        :param key: key to verify if contained
        :return: if MultiKeyDict contains the given key
        """
        keys = self._keySplit(key)
        return key in self._compositKeys(self) if len(keys) > 1 else dict.get(self, key, None) is not None

    def get(self, key: str, default: Any = None) -> Any:
        """
        get the value for hte given key or the default given value
        :param key: key to get hte value of
        :param default: default value if key not found
        :return: key value or default
        """
        return self[key] if key in self else default

    def compositKeys(self) -> List[str]:
        """
        Compiled list of keys
        :return: list of composite keys
        """
        return self._compositKeys(self)

    # helper functions
    def _compositKeys(self, obj: dict) -> List[str]:
        if isinstance(obj, self.__class__):
            tmp = []
            for key, val in obj.items():
                val_keys = self._compositKeys(val)
                if len(val_keys) > 0:
                    tmp.extend([f"{key}{self._sep}{k}" for k in val_keys])
                else:
                    tmp.append(key)
            return tmp
        else:
            return []

    def _keySplit(self, k):
        return list(filter(None, k.split(self._sep)))
