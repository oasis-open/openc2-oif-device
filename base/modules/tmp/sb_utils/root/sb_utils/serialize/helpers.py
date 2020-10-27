"""
Serialization encode/decode helper functions
"""
import bencode
import collections
import json
import os
import sexpdata
import tempfile
import xmltodict

from subprocess import Popen, PIPE
from typing import (
    Union
)

from ..general import (
    check_values,
    default_encode,
    floatByte
)


# Message Conversion helpers for Bencode
def bencode_encode(msg: dict) -> bytes:
    """
    Encode the given message to Bencode format
    :param msg: message to convert
    :return: Bencode formatted message
    """
    return bencode.bencode(default_encode(msg, {float: floatByte}))


def bencode_decode(msg: bytes) -> dict:
    """
    Decode the given message to Bencode format
    :param msg: message to convert
    :return: JSON formatted message
    """
    return default_encode(bencode.bdecode(msg), {bytes: floatByte})


# Message Conversion helpers for S-Expression
def _sp_decode(val):
    if isinstance(val, list) and isinstance(val[0], sexpdata.Symbol):
        rtn = {}
        for idx in range(0, len(val), 2):
            k = val[idx].value()
            k = k[1:] if k.startswith(":") else k
            rtn[k] = _sp_decode(val[idx + 1])
        return rtn
    return val


def sp_encode(msg: dict) -> str:
    """
    Encode the given message to S-Expression format
    :param msg: message to convert
    :return: S-Expression formatted message
    """
    return sexpdata.dumps(msg)


def sp_decode(msg: str) -> dict:
    """
    Decode the given message to JSON format
    :param msg: message to convert
    :return: JSON formatted message
    """
    rtn = sexpdata.loads(msg)
    return _sp_decode(rtn)


# Message Conversion helpers for XML
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


def xml_encode(msg: dict) -> str:
    """
    Encode the given message to XML format
    :param msg: message to convert
    :return: XML formatted message
    """
    return xmltodict.unparse({_xml_root(msg): msg})


def xml_decode(msg: str) -> dict:
    """
    Decode the given message to JSON format
    :param msg: message to convert
    :return: JSON formatted message
    """
    return _xml_root(_xml_to_dict(xmltodict.parse(msg)))


# Message Conversion helpers for VelocityPack (VPack)
def vpack_encode(msg: dict) -> bytes:
    rtn = b""
    with tempfile.NamedTemporaryFile(delete=True) as msg_tmp:
        with open(msg_tmp.name, "w") as f:
            f.write(json.dumps(msg))
        os.chmod(msg_tmp.name, 0o0777)
        msg_tmp.file.close()

        with tempfile.NamedTemporaryFile(delete=True) as enc_tmp:
            process = Popen(["json-to-vpack", msg_tmp.name, enc_tmp.name], stdout=PIPE, stderr=PIPE)
            _, _ = process.communicate()

            with open(enc_tmp.name, "rb") as f:
                rtn = f.read()

    return rtn


def vpack_decode(msg: bytes) -> dict:
    rtn = {}
    with tempfile.NamedTemporaryFile(delete=True) as msg_tmp:
        with open(msg_tmp.name, "wb") as f:
            f.write(msg)
        os.chmod(msg_tmp.name, 0o0777)
        msg_tmp.file.close()

        with tempfile.NamedTemporaryFile(delete=True) as dec_tmp:
            process = Popen(["vpack-to-json", msg_tmp.name, dec_tmp.name], stdout=PIPE, stderr=PIPE)
            _, _ = process.communicate()

            with open(dec_tmp.name, "rb") as f:
                rtn = json.load(f)

    return rtn
