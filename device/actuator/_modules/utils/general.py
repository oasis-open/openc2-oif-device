# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ipaddress
import json
import uuid

from typing import Any, List


def prefixUUID(pre="PREFIX", max=30):
    uid_max = max - (len(pre) + 10)
    uid = str(uuid.uuid4()).replace("-", "")[:uid_max]
    return f"{pre}-{uid}"[:max]


def safe_load(file_obj):
    try:
        return json.load(file_obj)
    except Exception as e:
        # print(f"{file_obj.name} - {e}")
        return {}


def valid_ip(ip):
    if isinstance(ip, (str, bytes)):
        try:
            if "/" in ip:
                # IP_Net
                ip = ipaddress.ip_network(ip, strict=False)
            else:
                # IP_Address
                ip = ipaddress.ip_address(ip)
            return ip
        except ValueError as e:
            print(e)

    return None


class MultiKeyDict(dict):
    def __init__(self, sep: str = ".", *args, **kwargs) -> None:
        super(MultiKeyDict, self).__init__(*args, **kwargs)
        self._sep = sep

        for k, v in dict(self).items():
            if self._sep in k:
                dict.__delitem__(self, k)
                keys = self._keySplit(k)
                dict.setdefault(self, keys[0], MultiKeyDict(sep=self._sep))[self._sep.join(keys[1:])] = v

    def __setitem__(self, key: str, val: Any) -> None:
        keys = self._keySplit(key)
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
        keys = self._keySplit(key)
        if len(keys) == 1:
            return dict.__getitem__(self, key)
        else:
            rtn = self
            for key in keys:
                rtn = dict.get(rtn, key, None)
            return rtn

    def __delitem__(self, key: str) -> None:
        keys = self._keySplit(key)
        if len(keys) == 1:
            dict.__delitem__(self, key)
        else:
            k = dict.get(self, keys[0], None)
            if k:
                k.__delitem__(self._sep.join(keys[1:]))

    def __contains__(self, item) -> bool:
        keys = self._keySplit(item)
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
                    tmp.extend([f"{key}{self._sep}{k}" for k in val_keys])
                else:
                    tmp.append(key)
            return tmp
        else:
            return []

    def _keySplit(self, k):
        return list(filter(None, k.split(self._sep)))
