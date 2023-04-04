"""
BINN (https://github.com/liteserver/binn) serialization/deserialization module
"""

__version__ = '0.9.5'
__all__ = [
    'dump',
    'dumps',
    'load',
    'loads',
    'CustomEncoder',
    'CustomDecoder',
    'BINNDecoder',
    'BINNEncoder'
]

__author__ = 'Miron Jakubowski <mijakubowski@gmail.com>'

from .encoder import BINNEncoder, CustomEncoder
from .decoder import BINNDecoder, CustomDecoder


def dumps(value, *custom_encoders):
    """
    Serialize `value` to BINN format and returns bytes
    """
    return BINNEncoder(None, *custom_encoders).encode_bytes(value)


def dump(value, fp, *custom_encoders):
    """
    Serialize `value` to BINN format and saves bytes to stream `fp`
    """
    BINNEncoder(fp, *custom_encoders).encode(value)


def loads(buffer, *custom_decoders):
    """
    Deserialize buffer in BINN format and return object
    """
    return BINNDecoder(buffer, None, *custom_decoders).decode()


def load(fp, *custom_decoders):
    """
    Deserialize stream and return object
    """
    return BINNDecoder(None, fp, *custom_decoders).decode()
