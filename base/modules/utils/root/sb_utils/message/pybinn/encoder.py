"""
Implementation of BINNEncoder
"""
from datetime import datetime, timedelta
from io import BytesIO
from struct import pack

from . import datatypes as types


class BINNEncoder:
    """
    BINN <https://github.com/liteserver/binn> encoder for Python
    """

    def __init__(self, fp=None, *custom_encoders):  # pylint: disable=keyword-arg-before-vararg
        self._buffer = fp
        if not self._buffer:
            self._buffer = BytesIO()
        self._custom_encoders = custom_encoders

    def encode_bytes(self, value):
        """
        Encode value and return bytes
        """
        self.encode(value)
        return self._buffer.getvalue()

    def encode(self, value):
        """
        Encode value to stream
        """
        if value is None:
            self._buffer.write(types.BINN_NULL)
            return
        if isinstance(value, str):
            self._encode_str(value)
            return
        if isinstance(value, int):
            self._encode_int(value)
            return
        if isinstance(value, bool):
            self._encode_bool(value)
            return
        if isinstance(value, float):
            self._encode_float(value)
            return
        if isinstance(value, bytes):
            self._encode_bytes(value)
            return
        if isinstance(value, list):
            self._encode_list(value)
            return
        if isinstance(value, dict):
            self._encode_dict(value)
            return
        if isinstance(value, datetime):
            self._encode_datetime(value)
            return
        # try use custom encoders when none type was recognized
        for encoder in self._custom_encoders:
            if not issubclass(type(encoder), CustomEncoder):
                raise TypeError(f"Type {type(encoder)} is not CustomerEncoder.")
            if isinstance(value, encoder.type):
                self._encode_custom_type(value, encoder)
                return

        raise TypeError(f"Invalid type for encode: {type(value)}")

    def _encode_str(self, value, data_type=types.BINN_STRING):
        size = len(value.encode('utf8'))
        self._buffer.write(data_type)
        self._buffer.write(self._to_varint(size))
        self._buffer.write(value.encode('utf8') + b'\0')

    def _encode_uint(self, value):
        # unsigned char (byte)
        if value < 0x100:
            self._buffer.write(types.BINN_UINT8)
            self._buffer.write(pack('B', value))
            return
        # unsigned short
        if value < 0x10000:
            self._buffer.write(types.BINN_UINT16)
            self._buffer.write(pack('H', value))
            return
        # unsigned int
        if value < 0x100000000:
            self._buffer.write(types.BINN_UINT32)
            self._buffer.write(pack('I', value))
            return
        # unsigned long
        if value < 0x10000000000000000:
            self._buffer.write(types.BINN_UINT64)
            self._buffer.write(pack('L', value))
            return
        raise OverflowError(f"Value to big {value:x}.")

    def _encode_int(self, value):
        if value >= 0:
            self._encode_uint(value)
            return
        # signed char
        if value >= -0x80:
            self._buffer.write(types.BINN_INT8)
            self._buffer.write(pack('b', value))
            return
        # short
        if value >= -0x8000:
            self._buffer.write(types.BINN_INT16)
            self._buffer.write(pack('h', value))
            return
        # int
        if value >= -0x80000000:
            self._buffer.write(types.BINN_INT32)
            self._buffer.write(pack('i', value))
            return
        # long
        if value >= -0x8000000000000000:
            self._buffer.write(types.BINN_INT64)
            self._buffer.write(pack('l', value))

    def _encode_bool(self, value):
        if value:
            self._buffer.write(types.BINN_TRUE)
        if not value:
            self._buffer.write(types.BINN_FALSE)

    def _encode_float(self, value, binn_type=None):
        if binn_type is None:
            binn_type = types.BINN_FLOAT64
        self._buffer.write(binn_type)
        self._buffer.write(pack('d', value))

    def _encode_bytes(self, value):
        self._buffer.write(types.BINN_BLOB)
        self._buffer.write(pack('I', len(value)))
        self._buffer.write(value)

    def _encode_datetime(self, value):
        timestamp = float((value - datetime(1970, 1, 1)) / timedelta(seconds=1))
        self._encode_float(timestamp, types.BINN_DATETIME)

    def _encode_list(self, value):
        with BytesIO() as buffer:
            for item in value:
                buffer.write(BINNEncoder().encode_bytes(item))

            self._buffer.write(types.BINN_LIST)
            self._buffer.write(BINNEncoder._to_varint(buffer.tell() + 3))
            self._buffer.write(BINNEncoder._to_varint(len(value)))
            self._buffer.write(buffer.getvalue())

    def _encode_dict(self, value):
        # set initial BINN type to handle empty dictionaries
        container_type = types.BINN_OBJECT

        with BytesIO() as buffer:
            for key in value:
                if isinstance(key, str):
                    if len(key) > 255:
                        raise OverflowError(f"Key '{key}' is to big. Max length is 255.")
                    buffer.write(pack('B', len(key)))
                    buffer.write(key.encode('utf8'))
                    buffer.write(BINNEncoder().encode_bytes(value[key]))
                elif isinstance(key, int):
                    container_type = types.BINN_MAP
                    buffer.write(pack('I', key))
                    buffer.write(BINNEncoder().encode_bytes(value[key]))
                elif isinstance(key, bytes):
                    if len(key) != types.PYBINN_MAP_SIZE:
                        raise OverflowError(f"Bytes key should be exactly {types.PYBINN_MAP_SIZE} bytes length.")
                    container_type = types.PYBINN_MAP
                    buffer.write(key)
                    buffer.write(BINNEncoder().encode_bytes(value[key]))
                else:
                    raise TypeError(f"Cannot serialize dictionary with key of type '{type(key)}'")

            self._buffer.write(container_type)
            self._buffer.write(BINNEncoder._to_varint(buffer.tell() + 3))
            self._buffer.write(BINNEncoder._to_varint(len(value)))
            self._buffer.write(buffer.getvalue())

    def _encode_custom_type(self, value, encoder):
        data = encoder.getbytes(value)
        self._buffer.write(encoder.datatype)
        self._buffer.write(BINNEncoder._to_varint(len(data)))
        self._buffer.write(data)

    @staticmethod
    def _to_varint(value):
        if value > 127:
            return pack('>I', value | 0x80000000)
        return pack('B', value)


class CustomEncoder:
    """
    Base class for handling encoding user types
    """

    def __init__(self, usr_type, data_type):
        # if custom data type is not BINN type
        if data_type in types.ALL:
            raise Exception(f"Data type {data_type} is defined as internal type.")

        self.type = usr_type
        self.datatype = data_type

    def getbytes(self, value):
        """
        Encode instance of custom type
        """
        raise NotImplementedError()
