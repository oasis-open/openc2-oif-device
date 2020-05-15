"""
Implementation of BINNDecoder
"""
import io

from datetime import datetime, timedelta
from functools import partial
from struct import unpack
from typing import (
    Callable,
    Dict,
    Union
)

from . import datatypes as types


class BINNDecoder:
    """
    BINN <https://github.com/liteserver/binn> decoder for Python
    """
    _decoders: Dict[bytes, Callable]

    def __init__(self, buffer=None, fp=None, *custom_decoders):  # pylint: disable=keyword-arg-before-vararg
        if buffer:
            self._buffer = io.BytesIO(buffer)
        if fp:
            self._buffer = fp
        self._custom_decoders = custom_decoders

        self._decoders = {
            types.BINN_STRING: self._decode_str,
            types.BINN_UINT8: partial(self._unpack, 'B', 1),
            types.BINN_INT8: partial(self._unpack, 'b', 1),
            types.BINN_UINT16: partial(self._unpack, 'H', 2),
            types.BINN_INT16:  partial(self._unpack, 'h', 2),
            types.BINN_UINT32:  partial(self._unpack, 'I', 4),
            types.BINN_INT32: partial(self._unpack, 'i', 4),
            types.BINN_UINT64: partial(self._unpack, 'L', 8),
            types.BINN_INT64: partial(self._unpack, 'l', 8),
            types.BINN_FLOAT64: partial(self._unpack, 'd', 8),
            types.BINN_BLOB:self._decode_bytes,
            types.BINN_DATETIME: self._decode_datetime,
            types.BINN_LIST: self._decode_list,
            types.BINN_OBJECT: self._decode_dict,
            types.BINN_MAP: self._decode_dict,
            types.PYBINN_MAP: self._decode_dict,
            types.BINN_TRUE: lambda: True,
            types.BINN_FALSE: lambda: False,
            types.BINN_NULL: lambda: None
        }

    def decode(self):
        """
        Decode date from buffer
        """
        binntype = self._buffer.read(1)
        decoder = self._decoders.get(binntype, None)
        if decoder and binntype in (types.BINN_OBJECT, types.BINN_MAP, types.PYBINN_MAP):
            return decoder(binntype)

        if decoder:
            return decoder()

        # if type was not found, try using custom decoders
        for decoder in self._custom_decoders:
            if not issubclass(type(decoder), CustomDecoder):
                raise TypeError("Type {} is not CustomDecoder.")
            if binntype == decoder.datatype:
                return self._decode_custom_type(decoder)

        raise TypeError(f"Invalid data format: {binntype}")

    def _decode_str(self):
        size = self._from_varint()
        value = self._buffer.read(size).decode('utf8')
        # Ready null terminator byte to advance position
        self._buffer.read(1)
        return value

    def _decode_bytes(self):
        size = unpack('I', self._buffer.read(4))[0]
        return self._buffer.read(size)

    def _decode_datetime(self):
        timestamp = float(unpack('d', self._buffer.read(8))[0])
        # datetime.utcfromtimestamp method in python3.3 has rounding issue (https://bugs.python.org/issue23517)
        return datetime(1970, 1, 1) + timedelta(seconds=timestamp)

    def _decode_list(self):
        # read container size
        self._from_varint()
        count = self._from_varint()
        result = []
        for _ in range(count):
            result.append(self.decode())
        return result

    def _decode_dict(self, binntype):
        # read container size
        self._from_varint()
        count = self._from_varint()
        result = {}
        for _ in range(count):
            if binntype == types.BINN_OBJECT:
                key_size = unpack('B', self._buffer.read(1))[0]
                key = self._buffer.read(key_size).decode('utf8')
            if binntype == types.BINN_MAP:
                key = unpack('I', self._buffer.read(4))[0]
            if binntype == types.PYBINN_MAP:
                key = self._buffer.read(types.PYBINN_MAP_SIZE)
            result[key] = self.decode()
        return result

    def _decode_custom_type(self, decoder):
        size = self._from_varint()
        return decoder.getobject(self._buffer.read(size))

    def _from_varint(self):
        value = unpack('B', self._buffer.read(1))[0]
        if value & 0x80:
            self._buffer.seek(self._buffer.tell() - 1)
            value = unpack('>I', self._buffer.read(4))[0]
            value &= 0x7FFFFFFF
        return value

    # Switch Helpers
    def _unpack(self, fmt: str, rb: int) -> Union[int, float]:
        return unpack(fmt, self._buffer.read(rb))[0]


class CustomDecoder:
    """
    Base class for handling decoding user types
    """

    def __init__(self, data_type):
        # check if custom data type is not BINN type
        if data_type in types.ALL:
            raise Exception(f"Data type {data_type} is defined as internal type.")

        self.datatype = data_type

    def getobject(self, data_bytes):
        """
        Decode object from bytes
        """
        raise NotImplementedError()
