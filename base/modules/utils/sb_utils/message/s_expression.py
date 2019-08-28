"""
Message Conversion functions for S-Expression
"""
import sexpdata


def _decode(val):
    if isinstance(val, list) and isinstance(val[0], sexpdata.Symbol):
        rtn = {}
        for idx in range(0, len(val), 2):
            k = val[idx].value()
            k = k[1:] if k.startswith(":") else k
            rtn[k] = _decode(val[idx + 1])
        return rtn
    return val


def encode(msg: dict) -> str:
    """
    Encode the given message to S-Expression format
    :param msg: message to convert
    :return: S-Expression formatted message
    """
    return sexpdata.dumps(msg)


def decode(msg: str) -> dict:
    """
    Decode the given message to JSON format
    :param msg: message to convert
    :return: JSON formatted message
    """
    rtn = sexpdata.loads(msg)
    return _decode(rtn)
