from enum import Enum


class SerialFormats(str, Enum):
    """
    The format of an OpenC2 Serialization
    """
    # Binary Format
    BINN = 'binn'
    BSON = 'bson'
    CBOR = 'cbor'
    MSGPACK = 'msgpack'
    SMILE = 'smile'
    VPACK = 'vpack'
    # Text Format
    BENCODE = 'bencode'
    JSON = 'json'
    S_EXPRESSION = 's_expression'
    TOML = 'toml'
    UBJSON = 'ubjson'
    XML = 'xml'
    YAML = 'yaml'

    @classmethod
    def from_name(cls, fmt: str):
        name = fmt.upper()
        if name in cls.__members__:
            return cls.__getattr__(name)
        raise ValueError(f'{name} is not a valid format name')

    @classmethod
    def from_value(cls, fmt: str):
        name = fmt.lower()
        for k, v in cls.__members__.items():
            if name == v:
                return cls.__getattr__(k)
        raise ValueError(f'{name} is not a valid format value')
