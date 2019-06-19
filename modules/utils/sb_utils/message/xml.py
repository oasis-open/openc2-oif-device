"""
Message Conversion functions
"""
import collections
import xmltodict

from dicttoxml import dicttoxml

from typing import (
    Any,
    Union
)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from ..general import safe_cast, toStr


def _xml_root(msg: dict) -> Union[dict, str]:
    """
    Get the message or determine the root key
    :param msg: message to find the root
    :return: root of message
    """
    if "command" in msg:
        return msg.get("command", {})

    if "response" in msg:
        return msg.get("response", {})

    if "action" in msg:
        return "command"

    if "status" in msg:
        return "response"

    return msg


def _check_values(val: Any) -> Union[bool, float, int, str]:
    val = toStr(val)

    if val.lower() in ("true", "false"):
        return safe_cast(val, bool,  val)

    if val.isdecimal() and "." in val:
        return safe_cast(val, float,  val)

    if val.isdigit():
        return safe_cast(val, int,  val)

    return val


def _xml_to_dict(xml: dict) -> dict:
    """
    Convert XML data to a dict
    :param xml: XML data to convert
    :return: dict repr of given XML
    """
    tmp = {}
    for k, v in xml.items():
        k = k[1:] if k.startswith("@") else k
        tmp[k] = _xml_to_dict(v) if isinstance(v, collections.OrderedDict) else _check_values(v)
    return tmp


def encode(val: dict) -> str:
    return dicttoxml(val, custom_root=_xml_root(val), attr_type=False).decode("utf-8")


def decode(val: str) -> dict:
    return _xml_root(_xml_to_dict(xmltodict.parse(val)))
