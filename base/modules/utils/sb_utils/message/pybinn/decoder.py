"""Implementation of BINNDecoder"""

import io
from struct import unpack
from datetime import datetime, timedelta

from . import datatypes as types


class BINNDecoder(object):
    """BINN <https://github.com/liteserver/binn> decoder for Python"""

    def __init__(self, buffer=None, fp=None, *custom_decoders):
        if buffer:
            self._buffer = io.BytesIO(buffer)
        if fp:
            self._buffer = fp
        self._custom_decoders = custom_decoders

    def decode(self):
        """Decode date from buffer"""
        binntype = self._buffer.read(1)
        if binntype == types.BINN_STRING:
            return self._decode_str()
        if binntype == types.BINN_UINT8:
            return unpack('B', self._buffer.read(1))[0]
        if binntype == types.BINN_INT8:
            return unpack('b', self._buffer.read(1))[0]
        if binntype == types.BINN_UINT16:
            return unpack('H', self._buffer.read(2))[0]
        if binntype == types.BINN_INT16:
            return unpack('h', self._buffer.read(2))[0]
        if binntype == types.BINN_UINT32:
            return unpack('I', self._buffer.read(4))[0]
        if binntype == types.BINN_INT32:
            return unpack('i', self._buffer.read(4))[0]
        if binntype == types.BINN_UINT64:
            return unpack('L', self._buffer.read(8))[0]
        if binntype == types.BINN_INT64:
            return unpack('l', self._buffer.read(8))[0]
        if binntype == types.BINN_FLOAT64:
            return unpack('d', self._buffer.read(8))[0]
        if binntype == types.BINN_BLOB:
            return self._decode_bytes()
        if binntype == types.BINN_DATETIME:
            return self._decode_datetime()
        if binntype == types.BINN_LIST:
            return self._decode_list()
        if binntype == types.BINN_OBJECT \
                or binntype == types.BINN_MAP \
                or binntype == types.PYBINN_MAP:
            return self._decode_dict(binntype)
        if binntype == types.BINN_TRUE:
            return True
        if binntype == types.BINN_FALSE:
            return False
        if binntype == types.BINN_NULL:
            return None
        # if type was not found, try using custom decoders
        for decoder in self._custom_decoders:
            if not issubclass(type(decoder), CustomDecoder):
                raise TypeError("Type {} is not CustomDecoder.")
            if binntype == decoder.datatype:
                return self._decode_custom_type(decoder)

        raise TypeError("Invalid data format: {}".format(binntype))

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
        for i in range(count):
            result.append(self.decode())
        return result

    def _decode_dict(self, binntype):
        # read container size
        self._from_varint()
        count = self._from_varint()
        result = {}
        for i in range(count):
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


class CustomDecoder(object):
    """Base class for handling decoding user types"""

    def __init__(self, data_type):
        # check if custom data type is not BINN type
        if data_type in types.ALL:
            raise Exception("Data type {} is defined as internal type.".format(data_type))

        self.datatype = data_type

    def getobject(self, data_bytes):
        """Decode object from bytes"""
        raise NotImplementedError()
