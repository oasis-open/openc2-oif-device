import copy
import json
import sys
import uuid

from io import BufferedIOBase, TextIOBase
from ipaddress import (
    ip_network,
    ip_address,
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network
)
from jsonschema import Draft7Validator, ValidationError
from typing import (
    Any,
    List,
    Union
)


def prefixUUID(pre: str = "PREFIX", max_len: int = 30) -> str:
    """
    Prefix a UUID to a set length
    :param pre: prefix
    :param max_len: maximum length of the string
    :return: prefixed UUID
    """
    uid_max = max_len - (len(pre) + 10)
    uid = str(uuid.uuid4()).replace("-", "")[:uid_max]
    return f"{pre}-{uid}"[:max_len]


def safe_load(file_obj: Union[str, BufferedIOBase, TextIOBase]) -> dict:
    """
    Safely load a json file
    :param file_obj: json file path/object to load
    :return: loaded json data
    """
    try:
        if isinstance(file_obj, (BufferedIOBase, TextIOBase)):
            return json.load(file_obj)

        if isinstance(file_obj, str):
            with open(file_obj, "rb") as f:
                return json.load(f)

    except Exception as e:
        return {}


def valid_ip(ip: Union[bytes, str]) -> Union[None, IPv4Address, IPv6Address, IPv4Network, IPv6Network]:
    """
    Validate and load an IP/Network
    :param ip: IP/Network string/bytes to load
    :return: None or loaded IP/Network
    """
    if isinstance(ip, (str, bytes)):
        try:
            return ip_network(ip, strict=False) if "/" in ip else ip_address(ip)
        except ValueError as e:
            print(e)
    return None


class ValidatorJSON(Draft7Validator):
    # Custom Methods
    def iter_errors_as(self, instance: dict, _type: str) -> list:
        if self._is_exported(_type):
            exp = self._get_definition(_type)
            exp_type = exp.get('type', '')
            if exp_type == 'object':
                tmp_schema = copy.deepcopy(self.schema)
                del tmp_schema['oneOf']
                del tmp_schema['definitions'][_type]
                tmp_schema.update(exp)

                return self.iter_errors(instance, _schema=tmp_schema)
            else:
                raise TypeError(f'field type object is expected, field type: {exp_type}')
        else:
            raise TypeError(f'field type is not an exported field')

    def is_valid_as(self, instance: dict, _type: str) -> bool:
        """
        Check if the instance is valid under the current schema
        :param instance: message to validate
        :param _type: type to validate against
        :return: bool - Valid/Invalid
        """
        try:
            self.validate_as(instance, _type)
            return True
        except ValidationError:
            return False

    def validate_as(self, instance: dict, _type: str):
        """
        Check if the instance is valid under the current schema
        :param instance: message to validate
        :param _type: type to validate against
        :return: ...
        """
        if self._is_exported(_type):
            exp = self._get_definition(_type)
            exp_type = exp.get('type', '')
            if exp_type == 'object':
                tmp_schema = copy.deepcopy(self.schema)
                del tmp_schema['oneOf']
                del tmp_schema['definitions'][_type]
                tmp_schema.update(exp)

                return self.validate(instance, _schema=tmp_schema)
            else:
                raise TypeError(f'field type object is expected, field type: {exp_type}')
        else:
            raise TypeError(f'field type is not an exported field')

    # Helper Methods
    def _is_exported(self, _type: str) -> bool:
        """
        Check if the given type if exported
        :param _type: name of type to check if exported
        :return: bool - type is exported type
        """
        exported = [exp.get('$ref', '') for exp in self.schema.get('oneOf', [])]
        return any([exp.endswith(f'{_type}') for exp in exported])

    def _get_definition(self, _type: str) -> dict:
        """
        Get the definition for the given type
        :param _type: type to get hte definition for
        :return: dict - type definition
        """
        return self.schema.get('definitions', {}).get(_type, {})

    def _toStr(self, s: Any) -> str:
        """
        Convert a given type to a default string
        :param s: item to convert to a string
        :return: converted string
        """
        return s.decode(sys.getdefaultencoding(), 'backslashreplace') if hasattr(s, 'decode') else str(s)

    def _default_encoding(self, itm: Any) -> Any:
        """
        Encode the given object/type to the default of the system
        :param itm: object/type to convert to the system default
        :return: system default converted object/type
        """
        if isinstance(itm, dict):
            return {self._toStr(k): self._default_encoding(v) for k, v in itm.items()}

        if isinstance(itm, list):
            return [self._default_encoding(i) for i in itm]

        if isinstance(itm, tuple):
            return (self._default_encoding(i) for i in itm)

        if isinstance(itm, (bytes, bytearray)):
            return self._toStr(itm)

        if isinstance(itm, (complex, int, float, object)):
            return itm

        return self._toStr(itm)


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
