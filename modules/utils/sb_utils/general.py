import json
import sys
import uuid

from typing import (
    Any,
    Callable,
    Dict,
    Type,
    Union
)


# Util Functions
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


def safe_json(msg: Union[dict, str], encoders: Dict[Type, Callable[[Any], Any]] = {}, *args, **kwargs) -> Union[dict, str]:
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

    msg = default_encode(msg, encoders)
    return json.dumps(msg, *args, **kwargs)


def check_values(val: Any) -> Any:
    """
    Check the value of given and attempt to convert it to a bool, int, float
    :param val: value to check
    :return: converted/original value
    """
    if isinstance(val, str):
        if val.lower() in ("true", "false"):
            return safe_cast(val, bool,  val)

        if val.isdecimal() and "." in val:
            return safe_cast(val, float,  val)

        if val.isdigit():
            return safe_cast(val, int,  val)

    return val


def default_encode(itm: Any, encoders: Dict[Type, Callable[[Any], Any]] = {}) -> Any:
    """
    Default encode the given object to the system default string
    :param itm: object to encode/decode,
    :param encoders: custom type encoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: default system encoded object
    """
    if isinstance(itm, tuple(encoders.keys())):
        return encoders[type(itm)](itm)

    if isinstance(itm, dict):
        return {k: default_encode(v) for k, v in itm.items()}

    if isinstance(itm, (list, tuple)):
        return type(itm)(default_encode(i) for i in itm)

    if isinstance(itm, (complex, int, float)):
        return itm

    if isinstance(itm, str):
        return check_values(itm)

    return toStr(itm)
