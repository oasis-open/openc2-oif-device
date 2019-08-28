"""
Message Conversion functions
"""
import base64
import bson
import cbor2
import json
import msgpack
import shutil
import ubjson
import yaml

from .. import (
    ext_dicts,
    general
)

from . import (
    avro,
    pybinn,
    pysmile,
    s_expression,
    xml
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
    from . import vpack
    optionals["encode"]["vpack"] = lambda v: base64.b64encode(vpack.encode(v)).decode("utf-8")
    optionals["decode"]["vpack"] = lambda v: vpack.decode(base64.b64decode(v if isinstance(v, bytes) else v.encode()))


serializations = ext_dicts.FrozenDict(
    encode=ext_dicts.FrozenDict(
        # avro=lambda v: avro.encode(v),
        binn=lambda v: base64.b64encode(pybinn.dumps(v)).decode("utf-8"),
        bson=lambda v: base64.b64encode(bson.dumps(v)).decode("utf-8"),
        cbor=lambda v: base64.b64encode(cbor2.dumps(v)).decode("utf-8"),
        json=lambda v: json.dumps(v),
        msgpack=lambda v: base64.b64encode(msgpack.packb(v, use_bin_type=True)).decode("utf-8"),
        s_expression=lambda v: s_expression.encode(v),
        # smile=lambda v: base64.b64encode(pysmile.encode(v)).decode("utf-8"),
        xml=lambda v: xml.encode(v),
        ubjson=lambda v: base64.b64encode(ubjson.dumpb(v)).decode("utf-8"),
        yaml=lambda v: yaml.dump(v, Dumper=Dumper),
        **optionals["encode"]
    ),
    decode=ext_dicts.FrozenDict(
        # avro=lambda v: avro.decode(v),
        binn=lambda v: pybinn.loads(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        bson=lambda v: bson.loads(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        cbor=lambda v: cbor2.loads(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        json=lambda v: json.loads(v),
        msgpack=lambda v: msgpack.unpackb(base64.b64decode(v if isinstance(v, bytes) else v.encode()), raw=False),
        s_expression=lambda v: s_expression.decode(v),
        # smile=lambda v: pysmile.decode(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        xml=lambda v: xml.decode(v),
        ubjson=lambda v: ubjson.loadb(base64.b64decode(v if isinstance(v, bytes) else v.encode())),
        yaml=lambda v: yaml.load(v, Loader=Loader),
        **optionals["decode"]
    )
)

del optionals


def encode_msg(msg: dict, enc: str) -> str:
    """
    Encode the given message using the serialization specified
    :param msg: message to encode
    :param enc: serialization to encode
    :return: encoded message
    """
    enc = enc.lower()
    msg = general.default_encode(msg)

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

    msg = serializations["decode"].get(enc, serializations.decode["json"])(msg)
    return general.default_decode(msg)
