from enum import Enum, EnumMeta
from typing import Tuple, Type, Union


class EnumMetaSB(EnumMeta):
    def __new__(mcs, name: str, bases: Tuple[Type], attrs: dict):
        if opts := attrs.get('_optional_values'):
            attrs.update(opts(mcs))
        return super(EnumMetaSB, mcs).__new__(mcs, name, bases, attrs)

    def __contains__(cls, item):
        return item in list(cls.__members__.values())


class EnumBase(Enum, metaclass=EnumMetaSB):
    @classmethod
    def from_name(cls, fmt: str) -> 'EnumBase':
        name = fmt.upper()
        for k, v in dict(cls.__members__).items():
            if name == k.upper():
                return v
        raise ValueError(f'{name} is not a valid name')

    @classmethod
    def from_value(cls, fmt: Union[int, str]) -> 'EnumBase':
        members = dict(cls.__members__)
        for k, v in members.items():
            if fmt == v:
                return cls.__getattr__(k)
        raise ValueError(f'{fmt} is not a valid value')
