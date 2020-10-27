from enum import Enum


class MessageType(int, Enum):
    """
    The type of an OpenC2 Message
    """
    Request = 144       # The initiator of a two-way message exchange.
    Response = 145      # A response linked to a request in a two-way message exchange.
    Notification = 146  # A (one-way) message that is not a request or response.  (Placeholder)

    @classmethod
    def from_name(cls, fmt: str):
        name = fmt.capitalize()
        if name in cls.__members__:
            return cls.__getattr__(name)
        raise ValueError(f'{name} is not a valid format name')

    @classmethod
    def from_value(cls, fmt: int):
        for k, v in cls.__members__.items():
            if fmt == v:
                return cls.__getattr__(k)
        raise ValueError(f'{fmt} is not a valid format value')


class SerialTypes(int, Enum):
    """
    The type of an OpenC2 Serialization
    """
    # Binary Format
    CBOR = 0
    # Text Format
    JSON = 128
    XML = 129
    # Extra
    # Bin
    BINN = 1
    BSON = 2
    MSGPACK = 3
    SMILE = 4
    VPACK = 5
    # Txt
    BENCODE = 130
    S_EXPRESSION = 131
    TOML = 132
    UBJSON = 133
    YAML = 134

    @classmethod
    def from_name(cls, fmt: str):
        name = fmt.upper()
        if name in cls.__members__:
            return cls.__getattr__(name)
        raise ValueError(f'{name} is not a valid format name')

    @classmethod
    def from_value(cls, fmt: int):
        for k, v in cls.__members__.items():
            if fmt == v:
                return cls.__getattr__(k)
        raise ValueError(f'{fmt} is not a valid format value')
