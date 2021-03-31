from shutil import which
from ..utils import EnumBase


class MessageType(int, EnumBase):
    """
    The type of an OpenC2 Message
    """
    Request = 144       # The initiator of a two-way message exchange.
    Response = 145      # A response linked to a request in a two-way message exchange.
    Notification = 146  # A (one-way) message that is not a request or response.  (Placeholder)


class SerialTypes(int, EnumBase):
    """
    The type of an OpenC2 Serialization
    """
    # Binary Format
    CBOR = 0
    # Text Format
    JSON = 128
    # Extra
    # Binary
    BINN = 1
    BSON = 2
    ION = 5
    MSGPACK = 3
    SMILE = 4
    # Text
    BENCODE = 130
    EDN = 135
    S_EXPRESSION = 131
    TOML = 132
    UBJSON = 133
    XML = 129
    YAML = 134

    def _optional_values(self):
        vals = {}
        # VPACK - Binary
        if which("json-to-vpack") and which("vpack-to-json"):
            vals['VPACK'] = 5
        return vals
