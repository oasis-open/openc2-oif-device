"""
Message Signature and validation
Functions should be name as `SERIALIZATION_sign` and `SERIALIZATION_verify`
Serialization should be the lowercase of the values specified in `../enums.py -> SerialTypes`
"""
from .json_signature import json_sign, json_verify

__all__ = [
    'json_sign',
    'json_verify'
]
