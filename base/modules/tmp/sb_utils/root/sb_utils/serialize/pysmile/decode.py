#!/usr/bin/env python
"""
SMILE Decode
"""
import json
import logging
import struct

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Union
from . import constants, util

log = logging.getLogger()
if not log.handlers:
    log.addHandler(logging.NullHandler())


class SMILEDecodeError(Exception):
    pass


class DecodeMode(int, Enum):
    HEAD = 0       # Waiting for magic header :)
    ROOT = 1       # Waiting for Root object
    ARRAY = 2      # In array context
    VALUE = 3      # Waiting for value
    KEY = 4        # Waiting for key
    DONE = 5       # Done -- remain here until reset
    BAD = 6        # Got a data error -- remain here until reset


@dataclass
class SmileHeader:
    version: int
    raw_binary: bool = True
    shared_keys: bool = True
    shared_values: bool = True


class SmileDecoder:
    input: bytearray
    output: List[Union[int, float, str]]
    mode: DecodeMode
    error: str
    index: int
    nested_depth: int
    in_array: List[bool]
    first_array_element: List[bool]
    first_key: List[bool]
    header: SmileHeader
    shared_key_strings: List[str]
    shared_value_strings: List[str]
    _decoders: Dict[DecodeMode, Callable]

    def __init__(self, smile: Union[bytes, str] = None):
        self.init(smile)
        self._decoders = {
            DecodeMode.HEAD: self._decode_header,
            DecodeMode.ROOT: self._decode_RAV,
            DecodeMode.ARRAY: self._decode_RAV,
            DecodeMode.VALUE: self._decode_RAV,
            DecodeMode.KEY: self._decode_key
        }

    def init(self, smile: Union[bytes, str] = None) -> None:
        # Input
        if smile:
            self.input = bytearray(smile if isinstance(smile, bytes) else bytes(smile, "UTF-8"))
        else:
            self.input = bytearray()

        # Output
        self.output = []

        # Current Decoder State
        self.mode = DecodeMode.HEAD

        # Error message
        del self.error

        # Current read index
        self.index = 0

        # current nest level
        self.nested_depth = 0

        # true if in array context
        self.in_array = [False] * 30

        # true if the next token is the first value of an array (used for printing)
        self.first_array_element = [False] * 30

        # true if the next token is the first key of an object (used for printing)
        self.first_key = [False] * 30

        # smile header
        del self.header

        # Cached Keys for back references
        self.shared_key_strings = []

        # Cached Values for back references
        self.shared_value_strings = []

    @staticmethod
    def _escape(o: Union[bytearray, bytes, str]) -> str:
        o = o.decode("utf-8") if isinstance(o, (bytearray, bytes)) else o
        return o.replace("\n", r"\n").replace("\"", r"\"")

    def get_value(self) -> str:  # bytes:
        return "".join(map(str, self.output))

    # Decoding methods
    def copy_key_string(self, n: int = 0) -> None:
        key_str = self._escape(self.input[self.index:self.index + n])
        if self.header.shared_keys:
            self.save_key_string(key_str)
        self.write(f"\"{key_str}\":")
        self.index += n

    def copy_shared_key_string(self) -> None:
        if not self.header.shared_keys:
            raise SMILEDecodeError("Cannot lookup shared key, sharing disabled!")
        try:
            sh_str = self.shared_key_strings[self.input[self.index - 1] - 0x40]
        except IndexError:
            log.debug("self.index: %d", self.index)
            log.debug("self.shared_key_strings: %s", self.shared_key_strings)
        else:
            self.write(f"\"{sh_str}\":")

    def copy_shared_value_string(self) -> None:
        if not self.header.shared_values:
            raise SMILEDecodeError("Cannot lookup shared value, sharing disabled!")
        try:
            svr = self.shared_value_strings[self.input[self.index - 1] - 1]
        except IndexError:
            log.debug("self.index: %d", self.index)
            log.debug("self.shared_value_strings: %s", self.shared_value_strings)
        else:
            self.write(f"\"{svr}\"")

    def copy_value_string(self, n: int = 0) -> None:
        val_str = self._escape(self.input[self.index:self.index + n])
        if self.header.shared_values:
            self.save_value_string(val_str)
        self.write(f"\"{val_str}\"")
        self.index += n

    def copy_variable_length_string(self) -> None:
        i = self.input.index(b"\xfc", self.index)
        self.write(f"\"{self._escape(self.input[self.index:i])}\"")
        self.index = i + 1

    def pull_bits(self, n: int) -> bytes:
        ret_s = b""
        for _ in range(abs(n)):
            byt = self.pull_byte()
            if byt is None:
                break
            ret_s += bytes([byt])
        return ret_s

    def pull_byte(self) -> Union[int, None]:
        if len(self.input) > self.index:
            rtn = self.input[self.index]
            self.index += 1
            return rtn
        self.mode = DecodeMode.DONE
        return None

    def save_key_string(self, key_str: str) -> None:
        log.debug("key_str: %s", key_str)
        self.shared_key_strings.append(key_str)

    def save_value_string(self, val_str: str) -> None:
        log.debug("val_str: %s", val_str)
        self.shared_value_strings.append(val_str)

    def varint_decode(self) -> int:
        smile_zzvarint_decode = 0
        tmp = self.input[self.index:]
        for _, ch in enumerate(tmp):
            self.index += 1
            if ch & 0x80:
                smile_zzvarint_decode <<= 6
                smile_zzvarint_decode |= (ch & 0x3F)
                break
            smile_zzvarint_decode <<= 7
            smile_zzvarint_decode |= ch
        return smile_zzvarint_decode

    def write(self, *args: Union[int, float, str]) -> None:
        if args:
            self.output.extend(args)

    def zzvarint_decode(self) -> None:
        self.write(util.zigzag_decode(self.varint_decode()))

    # Actual decoding
    def _decode_header(self) -> None:
        head = self.pull_bits(3)
        if not (head and head.startswith(constants.HEADER_BYTE_1 + constants.HEADER_BYTE_2 + constants.HEADER_BYTE_3)):
            self.mode = DecodeMode.BAD
            self.error = "Invalid Header!"
            return
        self.mode = DecodeMode.ROOT
        features = self.pull_byte()
        self.header = SmileHeader(
            version=features & constants.HEADER_BIT_VERSION,
            raw_binary=bool((features & constants.HEADER_BIT_HAS_RAW_BINARY) >> 2),
            shared_keys=bool(features & constants.HEADER_BIT_HAS_SHARED_NAMES),
            shared_values=bool((features & constants.HEADER_BIT_HAS_SHARED_STRING_VALUES) >> 1)
        )

    def _decode_RAV(self) -> None:
        if byt := self.pull_byte():
            log.debug(f"Pulled Byte: {byt:#02x}")  # pylint: disable=W1201,W1203

            if self.in_array[self.nested_depth]:
                if self.first_array_element[self.nested_depth]:
                    self.first_array_element[self.nested_depth] = False
                elif byt != constants.TOKEN_LITERAL_END_ARRAY:
                    self.write(",")

            if byt == constants.NULL_BIT:
                log.debug("Token: Null Bit (skip)")
            elif 0x01 <= byt <= 0x1F:
                log.debug("Token: Shared Value String")
                self.copy_shared_value_string()
            elif constants.TOKEN_LITERAL_EMPTY_STRING <= byt <= constants.TOKEN_LITERAL_TRUE:
                # Simple literals, numbers
                msg, b = {
                    constants.TOKEN_LITERAL_EMPTY_STRING: ("Token: Empty String", "\"\""),
                    constants.TOKEN_LITERAL_NULL: ("Token: Literal Null", "null"),
                    constants.TOKEN_LITERAL_FALSE: ("Token: Literal False", "false"),
                    constants.TOKEN_LITERAL_TRUE: ("Token: Literal True", "true"),
                }.get(byt)
                log.debug(msg)
                self.write(b)
            elif constants.TOKEN_PREFIX_INTEGER <= byt < constants.TOKEN_PREFIX_FP:
                # Integral numbers
                log.debug("Token: Integral Numbers")
                smile_value_length = byt & 0x03
                if smile_value_length < 2:
                    self.zzvarint_decode()
                elif smile_value_length == 2:
                    # BigInteger
                    log.warning("Not Yet Implemented: Value BigInteger")
                else:
                    # Reserved for future use
                    log.warning("Reserved: integral numbers with length >= 3")
            elif constants.TOKEN_PREFIX_FP <= byt <= 0x2B:
                # Floating point numbers
                if byt == constants.TOKEN_BYTE_FLOAT_32:
                    b1, b2, b3, b4, b5 = self.pull_bits(5)
                    byt = (b1 | (b2 << 7) | (b3 << 14) | (b4 << 21) | (b5 << 28))
                    try:
                        flt = util.bits_to_float(byt)
                    except struct.error:
                        flt = util.long_bits_to_float(byt)
                    self.write(flt)
                elif byt == constants.TOKEN_BYTE_FLOAT_64:
                    b1, b2, b3, b4, b5, b6, b7, b8, b9 = self.pull_bits(9)
                    byt = (b1 | (b2 << 7) | (b3 << 14) | (b4 << 21) | (b5 << 28) | (b6 << 35) | (b7 << 42) | (b8 << 49) | (b9 << 56))
                    flt = util.long_bits_to_float(byt)
                    self.write(flt)
                else:
                    log.warning("Not Yet Implemented")
            elif 0x2C <= byt <= 0x3F:
                # Reserved for future use
                log.warning("Reserved: 0x2C <= value <= 0x3F")
            elif 0x40 <= byt <= 0x5F or 0x80 <= byt <= 0x9F:
                # Tiny ASCII/Unicode
                log.debug("Token: Tiny ASCII/Unicode")
                smile_value_length = (byt & 0x1F) + 1
                self.copy_value_string(smile_value_length)
            elif 0x60 <= byt <= 0x7F or 0xA0 <= byt <= 0xBF:
                # Small ASCII/Unicode
                log.debug("Token: Small ASCII/Unicode")
                smile_value_length = (byt & 0x1F) + 33
                self.copy_value_string(smile_value_length)
            elif 0xC0 <= byt <= 0xDF:
                # Small Integers
                log.debug("Token: Small Integer")
                self.write(util.zigzag_decode(byt & 0x1F))
            else:
                # Misc binary / text / structure markers
                if constants.TOKEN_MISC_LONG_TEXT_ASCII <= byt < constants.TOKEN_MISC_LONG_TEXT_UNICODE:
                    # Long (variable length) ASCII text
                    log.debug("Token: Long (var length) ASCII Test")
                    self.copy_variable_length_string()
                elif constants.TOKEN_MISC_LONG_TEXT_UNICODE <= byt < constants.INT_MISC_BINARY_7BIT:
                    log.warning("Not Yet Implemented: Value Long Unicode")
                elif constants.INT_MISC_BINARY_7BIT <= byt < constants.TOKEN_PREFIX_SHARED_STRING_LONG:
                    log.warning("Not Yet Implemented: Value Long Shared String Reference")
                elif constants.TOKEN_PREFIX_SHARED_STRING_LONG <= byt < constants.HEADER_BIT_VERSION:
                    # Binary, 7-bit encoded
                    log.warning("Not Yet Implemented: Value Binary")
                elif constants.HEADER_BIT_VERSION <= byt < constants.TOKEN_LITERAL_START_ARRAY:
                    log.warning("Reserved: 0xF0 <= value <= 0xF8")
                elif byt == constants.TOKEN_LITERAL_START_ARRAY:
                    # START_ARRAY
                    log.debug("Token: Start Array")
                    self.write("[")
                    self.nested_depth += 1
                    self.in_array[self.nested_depth] = True
                    self.first_array_element[self.nested_depth] = True
                    self.first_key[self.nested_depth] = False
                elif byt == constants.TOKEN_LITERAL_END_ARRAY:
                    # END_ARRAY
                    log.debug("Token: End Array")
                    self.write("]")
                    self.nested_depth -= 1
                elif byt == constants.TOKEN_LITERAL_START_OBJECT:
                    # START_OBJECT
                    log.debug("Token: Start Object")
                    self.write("{")
                    self.nested_depth += 1
                    self.in_array[self.nested_depth] = False
                    self.first_array_element[self.nested_depth] = False
                    self.first_key[self.nested_depth] = True
                    self.mode = DecodeMode.KEY
                    return
                elif byt == constants.TOKEN_LITERAL_END_OBJECT:
                    log.debug("Token: End Object")
                    log.warning("Reserved: value == 0xFB")
                elif byt == constants.BYTE_MARKER_END_OF_STRING:
                    log.error("Found end-of-String marker (0xFC) in value mode")
                elif byt == constants.INT_MISC_BINARY_RAW:
                    log.warning("Not Yet Implemented: Raw Binary Data")
                elif byt == constants.BYTE_MARKER_END_OF_CONTENT:
                    log.debug("Token: End Marker")
                    self.mode = DecodeMode.DONE
                    return

            if not self.in_array[self.nested_depth]:
                self.mode = DecodeMode.KEY
            return

        log.debug("No bytes left to read!")
        self.mode = DecodeMode.DONE

    def _decode_key(self) -> None:
        byt = self.pull_byte()
        if byt in [None, constants.BYTE_MARKER_END_OF_CONTENT]:
            log.debug("No bytes left to read!")
            self.mode = DecodeMode.DONE
            return
        log.debug(f"Pulled Byte: {byt:#02x}")  # pylint: disable=W1201,W1203

        try:
            if self.first_key[self.nested_depth]:
                self.first_key[self.nested_depth] = False
            elif byt != constants.TOKEN_LITERAL_END_OBJECT:
                self.write(",")
        except IndexError:
            self.first_key.append(False)

        # Byte ranges are divided in 4 main sections (64 byte values each)
        if 0x00 <= byt <= 0x1F:
            log.warning("Reserved: 0x01 <= key <= 0x1F")
        elif byt == constants.TOKEN_LITERAL_EMPTY_STRING:
            # Empty String
            log.debug("Token: Literal Empty String")
            self.write("\"\"")
        elif constants.TOKEN_LITERAL_NULL <= byt <= 0x2F:
            log.warning("Reserved: 0x21 <= key <= 0x2F")
        elif constants.TOKEN_PREFIX_KEY_SHARED_LONG <= byt <= 0x33:
            # "Long" shared key name reference
            log.warning("Not Yet Implemented: Long Shared Key Name Reference")
        elif byt == 0x32:
            # Long (not-yet-shared) Unicode name, 64 bytes or more
            log.warning("Not Yet Implemented: Long Key Name")
        elif 0x35 <= byt <= 0x39:
            log.warning("Reserved: 0x35 <= key <= 0x39")
        elif byt == 0x3A:
            log.error("0x3A NOT allowed in Key mode")
        elif 0x3B <= byt <= 0x3F:
            log.warning("Reserved: 0x3B <= key <= 0x3F")
        elif constants.TOKEN_PREFIX_KEY_SHARED_SHORT <= byt <= 0x7F:
            # "Short" shared key name reference (1 byte lookup)
            log.debug("Token: Short Shared Key Name Reference")
            self.copy_shared_key_string()
        elif constants.TOKEN_PREFIX_KEY_ASCII <= byt <= 0xBF:
            # Short Ascii names
            # 5 LSB used to indicate lengths from 2 to 32 (bytes == chars)
            log.debug("Token: Short ASCII Name")
            smile_key_length = (byt & 0x1F) + 1
            self.copy_key_string(smile_key_length)
        elif constants.TOKEN_PREFIX_KEY_UNICODE <= byt <= constants.TOKEN_RESERVED:
            # Short Unicode names
            # 5 LSB used to indicate lengths from 2 to 57
            log.debug("Token: Short Unicode Name")
            smile_key_length = (byt - 0xC0) + 2
            self.copy_key_string(smile_key_length)
        elif constants.TOKEN_LITERAL_START_ARRAY <= byt <= constants.TOKEN_LITERAL_START_OBJECT:
            log.warning("Reserved: 0xF8 <= key <= 0xFA")
        elif byt == constants.TOKEN_LITERAL_END_OBJECT:
            log.debug("Token: Literal End Object")
            self.write("}")
            self.nested_depth -= 1
            try:
                in_arry = self.in_array[self.nested_depth]
            except IndexError:
                in_arry = False
            self.mode = DecodeMode.VALUE if in_arry else DecodeMode.KEY
            return
        elif byt >= constants.BYTE_MARKER_END_OF_STRING:
            log.warning("Reserved: key >= 0xFC")
        self.mode = DecodeMode.VALUE

    def decode(self, smile: Union[bytes, str] = None) -> Union[dict, list]:
        """
        Decode SMILE format string into a Python Object
        :param smile: SMILE formatted data string
        :returns: Decoded python object
        """
        if smile:
            self.init(smile)
        elif len(self.input) > 0:
            pass
        else:
            raise ValueError("Input not defined, cannot decode value")

        while self.mode not in (DecodeMode.BAD, DecodeMode.DONE):
            if decoder := self._decoders.get(self.mode, None):
                decoder()
                if self.mode == DecodeMode.BAD:
                    continue

            elif self.mode == DecodeMode.BAD:
                if self.error is None:
                    self.error = "Unknown Error!"
                break

            elif self.mode == DecodeMode.DONE:
                log.debug("Decoding Done!")
                break

        if self.mode == DecodeMode.BAD:
            raise SMILEDecodeError(f"Bad State: {self.error}", self.get_value())
        ret_val = self.get_value()
        try:
            jsonified = json.loads(ret_val)
        except (ValueError, UnicodeDecodeError) as err:
            msg = f"Unable to jsonify string: {ret_val}"
            log.exception(msg)
            raise SMILEDecodeError(msg, ret_val) from err
        return jsonified

    @classmethod
    def decode_smile(cls, smile: Union[bytes, str]) -> Union[dict, list]:
        """
        Decode SMILE format string into a Python Object
        :param smile: SMILE formatted data string
        :returns: Decoded python object
        """
        return cls().decode(smile)


def decode(smile: Union[bytes, str]) -> Union[dict, list]:
    """
    Decode SMILE format string into a Python Object
    :param smile: SMILE formatted data string
    :returns: Decoded python object
    """
    log.debug("Decoding: %s", smile)
    return SmileDecoder.decode_smile(smile)
