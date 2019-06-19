"""
Message Conversion functions
"""
import base64
import bson
import cbor2
import json
import msgpack
# import pybinn
# import pysmile
import re
# import pickle
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
        # avro=lambda v: v,
        # binn=lambda v: pybinn.dumps(v),
        bson=lambda v: bson.dumps(v),
        cbor=lambda v: cbor2.dumps(v),
        json=lambda v: json.dumps(v),
        msgpack=lambda v: msgpack.packb(v, use_bin_type=True),
        # pickle=lambda v: pickle.dumps(v),
        # protobuf=lambda v: v,
        # smile=lambda v: pysmile.encode(v),
        # thrift=lambda v: v,
        xml=lambda v: encode_xml(v),
        yaml=lambda v: yaml.dump(v, Dumper=Dumper),
    ),
    decode=FrozenDict(
        # avro=lambda v: v,
        # binn=lambda v: pybinn.loads(v),
        bson=lambda v: bson.loads(v),
        cbor=lambda v: cbor2.loads(v),
        json=lambda v: json.loads(v),
        msgpack=lambda v: msgpack.unpackb(v, raw=False),
        # pickle=lambda v: pickle.loads(v),
        # protobuf=lambda v: v,
        # smile=lambda v: pysmile.decode(v),
        # thrift=lambda v: v,
        xml=lambda v: decode_xml(v),
        yaml=lambda v: yaml.load(v, Loader=Loader),
    )
)


def encode_msg(msg: dict, enc: str, b64: bool = True) -> str:
    """
    Encode the given message using the serialization specified
    :param msg: message to encode
    :param enc: serialization to encode
    :param b64: encode byte string to base64 string, default True
    :return: encoded message
    """
    enc = enc.lower()

    if enc not in serializations.encode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.encode.keys())}")

    if not isinstance(msg, dict):
        raise TypeError(f"Message is not expected type {dict}, got {type(msg)}")

    if len(msg.keys()) == 0:
        raise KeyError("Message should have at minimum one key")

    encoded = serializations["encode"].get(enc, serializations.encode["json"])(msg)
    return base64.b64encode(encoded).decode() if isinstance(encoded, bytes) and b64 else encoded


def decode_msg(msg: str, enc: str, b64: bool = True) -> dict:
    """
    Decode the given message using the serialization specified
    :param msg: message to decode
    :param enc: serialization to decode
    :param b64: encode byte string to base64 string, default True
    :return: decoded message
    """
    enc = enc.lower()

    if isinstance(msg, dict):
        return msg

    if enc not in serializations.decode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.decode.keys())}")

    if not isinstance(msg, (bytes, bytearray, str)):
        raise TypeError(f"Message is not expected type {bytes}/{bytearray}/{str}, got {type(msg)}")

    if b64 and isinstance(msg, str) and re.match(r"^[a-zA-Z0-9+/]+?={0,3}$", msg):
        msg = base64.b64decode(msg)

    return serializations["decode"].get(enc, serializations.decode["json"])(msg)
