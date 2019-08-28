"""
Message Conversion functions for XML
"""
import collections
import xmltodict


from typing import Union

from ..general import check_values


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


def _xml_to_dict(xml: dict) -> dict:
    """
    Convert XML data to a dict
    :param xml: XML data to convert
    :return: dict repr of given XML
    """
    tmp = {}
    for k, v in xml.items():
        k = k[1:] if k.startswith(("@", "#")) else k
        if k in tmp:
            raise KeyError(f"Duplicate key from `attr_prefix` or `cdata_key` - {k}")
        tmp[k] = _xml_to_dict(v) if isinstance(v, collections.OrderedDict) else check_values(v)
    return tmp


def encode(msg: dict) -> str:
    """
    Encode the given message to XML format
    :param msg: message to convert
    :return: XML formatted message
    """
    return xmltodict.unparse({_xml_root(msg): msg})


def decode(msg: str) -> dict:
    """
    Decode the given message to JSON format
    :param msg: message to convert
    :return: JSON formatted message
    """
    return _xml_root(_xml_to_dict(xmltodict.parse(msg)))
