import base64
import binascii
import json
import re
import struct
import sys
import uuid

from datetime import datetime
from functools import partial
from types import (
    BuiltinFunctionType,
    BuiltinMethodType,
    FunctionType,
    MethodType,
    LambdaType
)
from typing import (
    Any,
    Callable,
    Dict,
    Type,
    Union
)


# Util Functions
def camelCase(s: str, delim: str = '_') -> str:
    s = s.split(delim)
    camel = s[0]
    camel += ''.join(map(str.capitalize, s[1:]))
    return camel


def toBytes(b: Any) -> bytes:
    """
    Convert a given type to a default byte string
    :param : item to convert to a byte string
    :return: converted byte string
    """
    return b if isinstance(b, bytes) else bytes(str(b), sys.getdefaultencoding())


def toStr(s: Any) -> str:
    """
    Convert a given type to a default string
    :param s: item to convert to a string
    :return: converted string
    """
    return s.decode(sys.getdefaultencoding(), 'backslashreplace') if hasattr(s, 'decode') else str(s)


def prefixUUID(pre: str = 'PREFIX', max_len: int = 30) -> str:
    """
    Prefix a uuid with the given prefix with a max length
    :param pre: prefix str
    :param max_len: max length of prefix + UUID
    :return: prefixed UUID
    """
    uid_max = max_len - (len(pre) + 10)
    uid = str(uuid.uuid4()).replace('-', '')[:uid_max]
    return f'{pre}-{uid}'[:max]


def safe_cast(val: Any, to_type: Type, default: Any = None) -> Any:
    """
    Cast the given value to the goven type safely without an exception being thrown
    :param val: value to cast
    :param to_type: type to cast as
    :param default: default value if casting fails
    :return: casted value or given default/None
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safe_json(msg: Union[dict, str], encoders: Dict[Type, Callable[[Any], Any]] = None, *args, **kwargs) -> Union[dict, str]:  # pylint: disable=keyword-arg-before-vararg
    """
    Load JSON data if given a str and able
    Dump JSON data otherwise, encoding using encoders & JSON Defaults
    :param msg: str JSON to attempt to load
    :param encoders: custom type encoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: loaded JSON data or original str
    """
    if isinstance(msg, str):
        try:
            return json.loads(msg, *args, **kwargs)
        except ValueError:
            return msg

    msg = default_encode(msg, encoders or {})
    return json.dumps(msg, *args, **kwargs)


def check_values(val: Any) -> Any:
    """
    Check the value of given and attempt to convert it to a bool, int, float
    :param val: value to check
    :return: converted/original value
    """
    if isinstance(val, str):
        if val.lower() in ("true", "false"):
            return safe_cast(val, bool, val)

        if re.match(r"^\d+\.\d+$", val):
            return safe_cast(val, float, val)

        if val.isdigit():
            return safe_cast(val, int, val)

    return val


def default_encode(itm: Any, encoders: Dict[Type, Callable[[Any], Any]] = None) -> Any:
    """
    Default encode the given object to the predefined types
    :param itm: object to encode/decode,
    :param encoders: custom type encoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: default system encoded object
    """
    if encoders and isinstance(itm, tuple(encoders.keys())):
        return encoders[type(itm)](itm)

    if isinstance(itm, dict):
        return {default_encode(k): default_encode(v, encoders) for k, v in itm.items()}

    if isinstance(itm, (list, set, tuple)):
        return type(itm)(default_encode(i, encoders) for i in itm)

    if isinstance(itm, (int, float)):
        return itm

    return toStr(itm)


def default_decode(itm: Any, decoders: Dict[Type, Callable[[Any], Any]] = None) -> Any:
    """
    Default decode the given object to the predefined types
    :param itm: object to encode/decode,
    :param decoders: custom type decoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: default system encoded object
    """
    print(itm)
    if decoders and isinstance(itm, tuple(decoders.keys())):
        return decoders[type(itm)](itm)

    if isinstance(itm, dict):
        return {default_decode(k, decoders): default_decode(v, decoders) for k, v in itm.items()}

    if isinstance(itm, (list, set, tuple)):
        return type(itm)(default_decode(i, decoders) for i in itm)

    if isinstance(itm, (int, float)):
        return itm

    if isinstance(itm, str):
        return check_values(itm)

    return itm


def isFunction(obj: Any) -> bool:
    """
    Determine if the given object is a function
    :param obj: object to check if function
    :return: bool if function
    """
    return isinstance(obj, (BuiltinFunctionType, BuiltinMethodType,  FunctionType, MethodType, LambdaType, partial))


def isBase64(sb: Union[bytes, str]) -> bool:
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except (binascii.Error, ValueError):
        return False


def floatByte(num: Union[float, bytes]) -> Union[float, bytes]:
    prefix = b"\x7E\x7F"  # `~ ` - tiddle, delete
    if isinstance(num, float):
        return prefix + struct.pack("!f", num)

    if isinstance(num, bytes) and num.startswith(prefix) and len(num) == 6:
        return struct.unpack("!f", num[1:])[0]

    return num


def floatString(num: Union[float, str]) -> Union[float, str]:
    prefix = "§£"
    if isinstance(num, float):
        return f"{prefix}{num}"

    if isinstance(num, str) and num.startswith(prefix) and num[1:].replace(".", "", 1).isdigit():
        return float(num[1:])

    return num


def unixTimeMillis(dt: datetime):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
