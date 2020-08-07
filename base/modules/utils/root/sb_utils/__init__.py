"""
Screaming Bunny Utils
Root Namespace
"""
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .amqp_tools import Consumer, Producer
from .general import prefixUUID, default_decode, default_encode, safe_cast, safe_json, toStr
from .ext_dicts import FrozenDict, ObjectDict, QueryDict
from .message import decode_msg, encode_msg, SerialFormats
from .message_obj import Message

__all__ = [
    # AMQP Tools
    'Consumer',
    'Producer',
    # General Utils
    'default_decode',
    'default_encode',
    'prefixUUID',
    'safe_cast',
    'safe_json',
    'toStr',
    # Extended Dictionaries
    'FrozenDict',
    'ObjectDict',
    'QueryDict',
    # Message Utils
    'Message',
    'decode_msg',
    'encode_msg',
    'SerialFormats'
]
