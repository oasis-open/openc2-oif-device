"""
Message Conversion functions
"""
import base64
import bson
import cbor2
import json
import msgpack
import yaml

from ..ext_dicts import FrozenDict

from .xml import (
    decode as decode_xml,
    encode as encode_xml
)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


serializations = FrozenDict(
    encode=FrozenDict(
        bson=lambda v: base64.b64encode(bson.dumps(v)).decode("utf-8"),
        cbor=lambda v: base64.b64encode(cbor2.dumps(v)).decode("utf-8"),
        json=lambda v: json.dumps(v),
        msgpack=lambda v: base64.b64encode(msgpack.packb(v, use_bin_type=True)).decode("utf-8"),
        xml=lambda v: encode_xml(v),
        yaml=lambda v: yaml.dump(v, Dumper=Dumper),
    ),
    decode=FrozenDict(
        bson=lambda v: bson.loads(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        cbor=lambda v: cbor2.loads(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        json=lambda v: json.loads(v),
        msgpack=lambda v: msgpack.unpackb(base64.b64decode(v if isinstance(v, bytes) else v.encode()), raw=False),
        xml=lambda v: decode_xml(v),
        yaml=lambda v: yaml.load(v, Loader=Loader),
    )
)


def encode_msg(msg: dict, enc: str) -> str:
    """
    Encode the given message using the serialization specified
    :param msg: message to encode
    :param enc: serialization to encode
    :return: encoded message
    """
    enc = enc.lower()

    if enc not in serializations.encode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.encode.keys())}")

    if not isinstance(msg, dict):
        raise TypeError(f"Message is not expected type {dict}, got {type(msg)}")

    if len(msg.keys()) == 0:
        raise KeyError("Message should have at minimum one key")

    return serializations["encode"].get(enc, serializations.encode["json"])(msg)


def decode_msg(msg: str, enc: str) -> dict:
    """
    Decode the given message using the serialization specified
    :param msg: message to decode
    :param enc: serialization to decode
    :return: decoded message
    """
    enc = enc.lower()

    if isinstance(msg, dict):
        return msg

    if enc not in serializations.decode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.decode.keys())}")

    if not isinstance(msg, (bytes, bytearray, str)):
        raise TypeError(f"Message is not expected type {bytes}/{bytearray}/{str}, got {type(msg)}")

    return serializations["decode"].get(enc, serializations.decode["json"])(msg)
