"""
Screaming Bunny Utils
Root Namespace
"""
from .amqp_tools import Consumer, Producer
from .auth import Auth
from .general import camelCase, destructure, toBytes, toStr, prefixUUID, default_decode, default_encode, safe_cast, safe_json
from .etcd_cache import EtcdCache, ReusableThread
from .ext_dicts import FrozenDict, ObjectDict, QueryDict
from .message import Message, MessageType
from .serialize import SerialFormats, decode_msg, encode_msg

__all__ = [
    # Authentication
    "Auth",
    # AMQP Tools
    'Consumer',
    'Producer',
    # General Utils
    'camelCase',
    'destructure',
    'toBytes',
    'toStr',
    'default_decode',
    'default_encode',
    'prefixUUID',
    'safe_cast',
    'safe_json',
    # Dictionaries
    'FrozenDict',
    'ObjectDict',
    'QueryDict',
    # Etcd
    'EtcdCache',
    'ReusableThread',
    # Message Utils
    'Message',
    'MessageType',
    'SerialFormats',
    'decode_msg',
    'encode_msg'
]
