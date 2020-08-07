"""
Message Conversion functions
"""
import base64
import bson
import cbor2
import json
import msgpack
import shutil
import toml
import ubjson
import yaml

from enum import Enum
from typing import Union
from . import (
    helpers,
    pybinn,
    pysmile
)
from .. import (
    ext_dicts,
    general
)


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

optionals = dict(
    encode={},
    decode={}
)

if shutil.which("json-to-vpack") and shutil.which("vpack-to-json"):
    optionals["encode"]["vpack"] = helpers.vpack_encode
    optionals["decode"]["vpack"] = helpers.vpack_decode


serializations = ext_dicts.FrozenDict(
    encode=ext_dicts.FrozenDict(
        binn=pybinn.dumps,
        bencode=helpers.bencode_encode,
        bson=bson.dumps,
        cbor=cbor2.dumps,
        json=json.dumps,
        msgpack=lambda m: msgpack.packb(m, use_bin_type=True),
        s_expression=helpers.sp_encode,
        smile=pysmile.encode,
        toml=toml.dumps,
        xml=helpers.xml_encode,
        ubjson=ubjson.dumpb,
        yaml=lambda m: yaml.dump(m, Dumper=Dumper),
        **optionals["encode"]
    ),
    decode=ext_dicts.FrozenDict(
        binn=pybinn.loads,
        bencode=helpers.bencode_decode,
        bson=bson.loads,
        cbor=cbor2.loads,
        json=json.loads,
        msgpack=msgpack.unpackb,
        s_expression=helpers.sp_decode,
        smile=pysmile.decode,
        toml=toml.loads,
        xml=helpers.xml_decode,
        ubjson=ubjson.loadb,
        yaml=lambda m: yaml.load(m, Loader=Loader),
        **optionals["decode"]
    )
)

SerialFormats = Enum('SerialFormats', {k.upper(): k for k in serializations['encode']})

del optionals


def encode_msg(msg: dict, enc: SerialFormats = SerialFormats.JSON, raw: bool = False) -> Union[bytes, str]:
    """
    Encode the given message using the serialization specified
    :param msg: message to encode
    :param enc: serialization to encode
    :param raw: message is in raw form (bytes/string) or safe string (base64 bytes as string)
    :return: encoded message
    """
    enc = enc.lower() if isinstance(enc, str) else enc.value
    msg = general.default_encode(msg)

    if enc not in serializations.encode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.encode.keys())}")

    if not isinstance(msg, dict):
        raise TypeError(f"Message is not expected type {dict}, got {type(msg)}")

    if len(msg.keys()) == 0:
        raise KeyError("Message should have at minimum one key")

    encoded = serializations["encode"].get(enc, serializations.encode["json"])(msg)
    if raw:
        return encoded
    return base64.b64encode(encoded).decode("utf-8") if isinstance(encoded, bytes) else encoded


def decode_msg(msg: Union[bytes, str], enc: SerialFormats, raw: bool = False) -> dict:
    """
    Decode the given message using the serialization specified
    :param msg: message to decode
    :param enc: serialization to decode
    :param raw: message is in raw form (bytes/string) or safe string (base64 bytes as string)
    :return: decoded message
    """
    enc = enc.lower() if isinstance(enc, str) else enc.value

    if isinstance(msg, dict):
        return msg

    if enc not in serializations.decode:
        raise ReferenceError(f"Invalid encoding specified, must be one of {', '.join(serializations.decode.keys())}")

    if not isinstance(msg, (bytes, bytearray, str)):
        raise TypeError(f"Message is not expected type {bytes}/{bytearray}/{str}, got {type(msg)}")

    if not raw and general.isBase64(msg):
        msg = base64.b64decode(msg if isinstance(msg, bytes) else msg.encode())

    msg = serializations["decode"].get(enc, serializations.decode["json"])(msg)
    return general.default_encode(msg, {bytes: bytes.decode})
