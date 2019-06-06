"""
Message Conversion functions
"""
import base64
import cbor2
import collections
import json
import xmltodict
import yaml

from dicttoxml import dicttoxml
from typing import Union

from .ext_dicts import FrozenDict

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def _xml_root(msg):
    """
    Get the message or determine the root key
    :param msg: message to find the root
    :return: root of message
    """
    if "message" in msg:
        return msg.get("message", {})

    if "response" in msg:
        return msg.get("response", {})

    if "action" in msg:
        return "message"

    if "status" in msg:
        return "response"

    return msg


def _xml_to_dict(xml):
    """
    Convert XML data to a dict
    :param xml: XML data to convert
    :return: dict repr of given XML
    """
    tmp = {}
    for k, v in xml.items():
        a = k[1:] if k.startswith("@") else k
        tmp[a] = _xml_to_dict(v) if isinstance(v, collections.OrderedDict) else v
    return tmp


serializations = FrozenDict(
    encode=FrozenDict(
        cbor=lambda v: base64.b64encode(cbor2.dumps(v)).decode("utf-8"),
        json=lambda v: json.dumps(v),
        xml=lambda v: dicttoxml(v, custom_root=_xml_root(v), attr_type=False).decode("utf-8"),
        yaml=lambda v: yaml.dump(v, Dumper=Dumper),
    ),
    decode=FrozenDict(
        cbor=lambda v: cbor2.loads(base64.b64decode(v if type(v) is bytes else v.encode())),
        json=lambda v: json.loads(v),
        xml=lambda v: _xml_root(_xml_to_dict(xmltodict.parse(v))),
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
