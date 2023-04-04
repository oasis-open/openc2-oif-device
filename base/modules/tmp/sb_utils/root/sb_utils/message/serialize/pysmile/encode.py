"""
SMILE Encode
"""
import copy
import decimal
import logging
import struct

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Type, Union
from . import constants, util

log = logging.getLogger()
if not log.handlers:
    log.addHandler(logging.NullHandler())


class SMILEEncodeError(Exception):
    pass


@dataclass
class SharedStringNode:
    """
    Helper class used for keeping track of possibly shareable String references (for field names
    and/or short String values)
    """
    value: Union[bytes, str]
    nxt: Any


class SmileEncoder:
    """
    To simplify certain operations, we require output buffer length
    to allow outputting of contiguous 256 character UTF-8 encoded String
    value. Length of the longest UTF-8 code point (from Java char) is 3 bytes,
    and we need both initial token byte and single-byte end marker
    so we get following value.

    Note: actually we could live with shorter one; absolute minimum would be for encoding
    64-character Strings.
    """
    encode_as_7bit: bool
    seen_string_count: int
    output: bytearray
    share_keys: bool
    share_values: bool
    shared_keys: List[Union[SharedStringNode, None]]
    shared_values: List[Union[SharedStringNode, None]]
    _encoders: Dict[Type, Callable]

    def __init__(self, shared_keys: bool = True, shared_values: bool = True, encode_as_7bit: bool = True):
        """
        SmileEncoder Initializer
        :param encode_as_7bit: (optional - Default: `True`) Encode raw data as 7-bit
        :param shared_keys: (optional - Default: `True`) Shared Key String References
        :param shared_values: (optional - Default: `True`) Shared Value String References
        """
        # Encoded data
        self.output = bytearray()

        # Shared Key Strings
        self.shared_keys = []

        # Shared Value Strings
        self.shared_values = []

        self.share_keys = bool(shared_keys)
        self.share_values = bool(shared_values)
        self.encode_as_7bit = bool(encode_as_7bit)

        # Encoder Switch
        self._encoders = {
            bool: self.write_boolean,
            dict: self._encode_dict,
            float: self.write_number,
            int: self.write_number,
            list: self._encode_array,
            str: self.write_string,
            tuple: self._encode_array,
            set: self._encode_array,
            None: self.write_null
        }

    def write_header(self) -> None:
        """
        Method that can be called to explicitly write Smile document header.
        Note that usually you do not need to call this for first document to output,
        but rather only if you intend to write multiple root-level documents
        with same generator (and even in that case this is optional thing to do).
        As a result usually only {@link SmileFactory} calls this method.
        """
        last = constants.HEADER_BYTE_4
        if self.share_keys:
            last |= constants.HEADER_BIT_HAS_SHARED_NAMES
        if self.share_values:
            last |= constants.HEADER_BIT_HAS_SHARED_STRING_VALUES
        if not self.encode_as_7bit:
            last |= constants.HEADER_BIT_HAS_RAW_BINARY
        self.write_bytes(constants.HEADER_BYTE_1, constants.HEADER_BYTE_2, constants.HEADER_BYTE_3, int(last))

    def write_ender(self) -> None:
        """
        Write optional end marker (BYTE_MARKER_END_OF_CONTENT - 0xFF)
        """
        self.write_byte(constants.BYTE_MARKER_END_OF_CONTENT)

    # Encoding writers
    def write_null(self) -> None:
        """
        Generated source for method writeNull
        """
        self.write_byte(constants.TOKEN_LITERAL_NULL)

    # Binary writers
    def write_7bit_binary(self, data: Union[bytes, str], offset: int = 0) -> None:
        l = len(data)
        self.write_positive_vint(l)
        while l >= 7:
            i = data[offset]
            offset += 1
            for x in range(1, 7):
                self.write_byte(int((i >> x) & 0x7F))
                i = (i << 8) | (data[offset + x] & 0xFF)
                offset += 1
            self.write_bytes(int((i >> 7) & 0x7F), int(i & 0x7F))
            l -= 7
        #  and then partial piece, if any
        if l > 0:
            i = data[offset]
            offset += 1
            self.write_byte(int(i >> 1) & 0x7F)
            if l > 1:
                i = ((i & 0x01) << 8) | (data[offset] & 0xFF)
                offset += 1

                #  2nd
                self.write_byte(int(i >> 2) & 0x7F)
                if l > 2:
                    i = ((i & 0x03) << 8) | (data[offset] & 0xFF)
                    offset += 1
                    #  3rd
                    self.write_byte(int(i >> 3) & 0x7F)
                    if l > 3:
                        i = ((i & 0x07) << 8) | (data[offset] & 0xFF)
                        offset += 1
                        #  4th
                        self.write_byte(int(i >> 4) & 0x7F)
                        if l > 4:
                            i = ((i & 0x0F) << 8) | (data[offset] & 0xFF)
                            offset += 1
                            #  5th
                            self.write_byte(int(i >> 5) & 0x7F)
                            if l > 5:
                                i = ((i & 0x1F) << 8) | (data[offset] & 0xFF)
                                offset += 1
                                #  6th
                                self.write_byte(int(i >> 6) & 0x7F)
                                self.write_byte(int(i & 0x3F))
                                #  last 6 bits
                            else:
                                self.write_byte(int(i & 0x1F))
                                #  last 5 bits
                        else:
                            self.write_byte(int(i & 0x0F))
                            #  last 4 bits
                    else:
                        self.write_byte(int(i & 0x07))
                        #  last 3 bits
                else:
                    self.write_byte(int(i & 0x03))
                    #  last 2 bits
            else:
                self.write_byte(int(i & 0x01))
                #  last bit

    def write_binary(self, data: bytes) -> None:
        """
        Write Data
        :param data: Data
        """
        if data is None:
            self.write_null()
            return
        if self.encode_as_7bit:
            self.write_byte(constants.TOKEN_MISC_BINARY_7BIT)
            self.write_7bit_binary(data)
        else:
            self.write_byte(constants.TOKEN_MISC_BINARY_RAW)
            self.write_positive_vint(len(data))
            self.write_bytes(data)

    def write_byte(self, c: Union[bytes, int, str]) -> None:
        """
        Write byte
        :param c: byte
        """
        if isinstance(c, (bytearray, bytes)):
            pass
        elif isinstance(c, str):
            c = c.encode("utf-8")
        elif isinstance(c, float):
            c = str(c)
        elif isinstance(c, int):
            c = struct.pack("B", c)
        else:
            raise ValueError(f"Invalid type for param 'c' - {type(c)}!")
        self.output.extend(c)

    def write_bytes(self, *args: Union[bytes, int, str]) -> None:
        """
        Write bytes
        :param args: args
        """
        for arg in args:
            self.write_byte(arg)

    # Boolean writers
    def write_boolean(self, state: bool) -> None:
        """
        Write Boolean
        :param state: Bool state
        """
        self.write_byte(state and constants.TOKEN_LITERAL_TRUE or constants.TOKEN_LITERAL_FALSE)

    # String writers
    def write_string(self, text: str) -> None:
        """
        Write String
        :param text: String text
        """
        if text is None:
            self.write_null()
            return
        if not text:
            self.write_byte(constants.TOKEN_LITERAL_EMPTY_STRING)
            return
        # Longer string handling off-lined
        if len(text) > constants.MAX_SHARED_STRING_LENGTH_BYTES:
            self.write_non_shared_string(text)
            return

        # Then: is it something we can share?
        if self.share_values:
            ix = self._find_seen_string_value(text)
            if ix >= 0:
                self.write_shared_string_value_reference(ix)
                return

        if len(text) <= constants.MAX_SHORT_VALUE_STRING_BYTES:
            if self.share_values:
                self._add_seen_string_value(text)
            self.write_bytes(int(constants.TOKEN_PREFIX_TINY_ASCII - 1) + len(text), text)
        else:
            self.write_bytes(constants.TOKEN_BYTE_LONG_STRING_ASCII, text, constants.BYTE_MARKER_END_OF_STRING)

    # Object writers
    def write_end_object(self) -> None:
        """
        Write end object token
        """
        self.write_byte(constants.TOKEN_LITERAL_END_OBJECT)

    def write_field_name(self, name: Union[bytes, str]) -> None:
        """
        Write Field Name
        :param name: Name
        """
        str_len = len(name)
        if not name:
            self.write_byte(constants.TOKEN_KEY_EMPTY_STRING)
            return

        # First: is it something we can share?
        if self.share_keys:
            ix = self._find_seen_name(name)
            if ix >= 0:
                self.write_shared_name_reference(ix)
                return

        if str_len > constants.MAX_SHORT_NAME_UNICODE_BYTES:
            # can not be a 'short' String; off-line (rare case)
            self.write_non_short_field_name(name)
            return

        if str_len <= constants.MAX_SHORT_NAME_ASCII_BYTES:
            self.write_bytes(int((constants.TOKEN_PREFIX_KEY_ASCII - 1) + str_len), name)
        else:
            self.write_bytes(constants.TOKEN_KEY_LONG_STRING, name, constants.BYTE_MARKER_END_OF_STRING)

        if self.share_keys:
            self._add_seen_name(name)

    def write_start_object(self) -> None:
        """
        Write start object token
        """
        self.write_byte(constants.TOKEN_LITERAL_START_OBJECT)

    def write_string_field(self, name: str, value: str) -> None:
        """
        Write String Field
        :param name: Name
        :param value: Value
        """
        self.write_field_name(name)
        self.write_string(value)

    # Array writers
    def write_end_array(self) -> None:
        """
        Write end array token
        """
        self.write_byte(constants.TOKEN_LITERAL_END_ARRAY)

    def write_start_array(self) -> None:
        """
        Write start array token
        """
        self.write_byte(constants.TOKEN_LITERAL_START_ARRAY)

    # Reference writers
    def write_shared_name_reference(self, ix: int) -> None:
        """
        Write Shared Name Ref
        :param ix: Index
        """
        if ix >= len(self.shared_keys) - 1:
            raise ValueError(f"Trying to write shared name with index {ix} but have only seen {len(self.shared_keys)}!")
        if ix < 64:
            self.write_byte(int(constants.TOKEN_PREFIX_KEY_SHARED_SHORT + ix))
        else:
            self.write_bytes(int(constants.TOKEN_PREFIX_KEY_SHARED_LONG + (ix >> 8)), int(ix))

    def write_shared_string_value_reference(self, ix: int) -> None:
        """
        Write shared string
        :param int ix: Index
        """
        if ix > len(self.shared_values) - 1:
            raise ValueError(f"Internal error: trying to write shared String value with index {ix}; but have only seen {len(self.shared_values)} so far!")
        if ix < 31:
            #  add 1, as byte 0 is omitted
            self.write_byte(constants.TOKEN_PREFIX_SHARED_STRING_SHORT + 1 + ix)
        else:
            self.write_bytes(constants.TOKEN_PREFIX_SHARED_STRING_LONG + (ix >> 8), int(ix))

    # Numeric Writers
    def write_big_number(self, i: str) -> None:
        """
        Write Big Number
        :param i: Big Number
        """
        if i is None:
            self.write_null()
        else:
            self.write_byte(constants.TOKEN_BYTE_BIG_INTEGER)
            self.write_7bit_binary(bytearray(str(i)))

    def write_decimal_number(self, num: str) -> None:
        """
        Write decimal
        :param num: String of a decimal number
        """
        if num is None:
            self.write_null()
        else:
            self.write_number(decimal.Decimal(num))

    def write_int(self, i: int) -> None:
        #  First things first: let's zigzag encode number
        i = util.zigzag_encode(i)
        if util.is_int32(i):
            #  tiny (single byte) or small (type + 6-bit value) number?
            if 0x3F >= i >= 0:
                if i <= 0x1F:
                    self.write_byte(int(constants.TOKEN_PREFIX_SMALL_INT + i))
                else:
                    # nope, just small, 2 bytes (type, 1-byte zigzag value) for 6 bit value
                    self.write_bytes(constants.TOKEN_BYTE_INT_32, int(0x80 + i))
                return
            #  Ok: let's find minimal representation then
            b0 = int(0x80 + (i & 0x3F))
            i >>= 6
            if i <= 0x7F:
                #  13 bits is enough (== 3 byte total encoding)
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b0)
                return
            b1 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b1, b0)
                return
            b2 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b2, b1, b0)
                return
            #  no, need all 5 bytes
            b3 = int(i & 0x7F)
            self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i >> 7), b3, b2, b1, b0)
        else:
            #  4 can be extracted from lower int
            b0 = int(0x80 + (i & 0x3F))
            #  sign bit set in the last byte
            b1 = int((i >> 6) & 0x7F)
            b2 = int((i >> 13) & 0x7F)
            b3 = int((i >> 20) & 0x7F)
            #  fifth one is split between ints:
            i = util.bsr(i, 27)
            b4 = int(i & 0x7F)
            #  which may be enough?
            i = int(i >> 7)
            if i == 0:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, b4, b3, b2, b1, b0)
                return
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b4, b3, b2, b1, b0)
                return
            b5 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b5, b4, b3, b2, b1, b0)
                return
            b6 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b6, b5, b4, b3, b2, b1, b0)
                return
            b7 = int((i & 0x7F))
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b7, b6, b5, b4, b3, b2, b1, b0)
                return
            b8 = int(i & 0x7F)
            i >>= 7
            #  must be done, with 10 bytes! (9 * 7 + 6 == 69 bits; only need 63)
            self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b8, b7, b6, b5, b4, b3, b2, b1, b0)

    def write_integral_number(self, num: str, neg: bool = False) -> None:
        """
        Write Int
        :param num: String of an integral number
        :param neg: Is the value negative
        """
        if num is None:
            self.write_null()
        else:
            num_len = len(num)
            if neg:
                num_len -= 1
            # try:
            if num_len <= 18:
                self.write_number(int(num))
            else:
                self.write_big_number(num)

    def write_non_shared_string(self, text: Union[bytes, str]) -> None:
        """
        Helper method called to handle cases where String value to write is known to be long
        enough not to be shareable
        :param text: Text
        """
        if len(text) <= constants.MAX_SHORT_VALUE_STRING_BYTES:
            self.write_bytes(int(constants.TOKEN_PREFIX_TINY_ASCII - 1) + len(text), text)
        else:
            self.write_bytes(constants.TOKEN_MISC_LONG_TEXT_ASCII, text, constants.BYTE_MARKER_END_OF_STRING)

    def write_non_short_field_name(self, name: str) -> None:
        """
        Write nonshort field name
        :param name: Name
        """
        self.write_byte(constants.TOKEN_KEY_LONG_STRING)
        try:
            utf_8_name = name.encode("utf-8")
        except UnicodeEncodeError:
            utf_8_name = name
        self.write_bytes(utf_8_name)
        if self.share_keys:
            self._add_seen_name(name)
        self.write_byte(constants.BYTE_MARKER_END_OF_STRING)

    def write_number(self, num: Union[int, float, str, decimal.Decimal]) -> None:
        """
        Write Number
        :param num: number
        """
        if isinstance(num, (float, decimal.Decimal)):
            self.write_number_decimal(num)
        if isinstance(num, int):
            self.write_number_int(num)
        if isinstance(num, str):
            self.write_number_str(num)

    def write_number_decimal(self, d: Union[float, decimal.Decimal]) -> None:
        if isinstance(d, decimal.Decimal):
            self.write_byte(constants.TOKEN_BYTE_BIG_DECIMAL)
            scale = d.as_tuple().exponent
            self.write_signed_vint(scale)
            self.write_7bit_binary(bytearray(str(d.to_integral_value())))
            return
        try:
            d = util.float_to_bits(d)
            self.write_bytes(
                constants.TOKEN_BYTE_FLOAT_32,
                int(d & 0x7F),
                *[(d >> 7 * i) & 0x7F for i in range(1, 5)]
            )
        except struct.error:
            d = util.float_to_raw_long_bits(d)
            self.write_bytes(
                constants.TOKEN_BYTE_FLOAT_64,
                int(d & 0x7F),
                *[(d >> 7 * i) & 0x7F for i in range(1, 10)]
            )

    def write_number_int(self, i: int) -> None:
        #  First things first: let's zigzag encode number
        i = util.zigzag_encode(i)
        if util.is_int32(i):
            #  tiny (single byte) or small (type + 6-bit value) number?
            if 0x3F >= i >= 0:
                if i <= 0x1F:
                    self.write_byte(int(constants.TOKEN_PREFIX_SMALL_INT + i))
                else:
                    # nope, just small, 2 bytes (type, 1-byte zigzag value) for 6 bit value
                    self.write_bytes(constants.TOKEN_BYTE_INT_32, int(0x80 + i))
                return
            #  Ok: let's find minimal representation then
            b0 = int(0x80 + (i & 0x3F))
            i >>= 6
            if i <= 0x7F:
                #  13 bits is enough (== 3 byte total encoding)
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b0)
                return
            b1 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b1, b0)
                return
            b2 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i), b2, b1, b0)
                return
            #  no, need all 5 bytes
            b3 = int(i & 0x7F)
            self.write_bytes(constants.TOKEN_BYTE_INT_32, int(i >> 7), b3, b2, b1, b0)
        else:
            #  4 can be extracted from lower int
            b0 = int(0x80 + (i & 0x3F))
            #  sign bit set in the last byte
            b1 = int((i >> 6) & 0x7F)
            b2 = int((i >> 13) & 0x7F)
            b3 = int((i >> 20) & 0x7F)
            #  fifth one is split between ints:
            i = util.bsr(i, 27)
            b4 = int(i & 0x7F)
            #  which may be enough?
            i = int(i >> 7)
            if i == 0:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, b4, b3, b2, b1, b0)
                return
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b4, b3, b2, b1, b0)
                return
            b5 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b5, b4, b3, b2, b1, b0)
                return
            b6 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b6, b5, b4, b3, b2, b1, b0)
                return
            b7 = int((i & 0x7F))
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b7, b6, b5, b4, b3, b2, b1, b0)
                return
            b8 = int(i & 0x7F)
            i >>= 7
            #  must be done, with 10 bytes! (9 * 7 + 6 == 69 bits; only need 63)
            self.write_bytes(constants.TOKEN_BYTE_INT_64, int(i), b8, b7, b6, b5, b4, b3, b2, b1, b0)

    def write_number_str(self, s: str) -> None:
        if s:
            s = s.strip("-")
            if s.isdigit():
                self.write_integral_number(s, s.startswith("-"))
            else:
                self.write_decimal_number(s)
        else:
            self.write_null()

    def write_positive_vint(self, i: int) -> None:
        """
        Helper method for writing a 32-bit positive (really 31-bit then) value
        Value is NOT zigzag encoded (since there is no sign bit to worry about)
        :param i: Int
        """
        #  At most 5 bytes (4 * 7 + 6 bits == 34 bits)
        b0 = int(0x80 + (i & 0x3F))
        i >>= 6
        if i <= 0x7F:
            #  6 or 13 bits is enough (== 2 or 3 byte total encoding)
            if i > 0:
                self.write_byte(int(i))
            self.write_byte(b0)
            return
        b1 = int(i & 0x7F)
        i >>= 7
        if i <= 0x7F:
            self.write_bytes(int(i), b1, b0)
        else:
            b2 = int(i & 0x7F)
            i >>= 7
            if i <= 0x7F:
                self.write_bytes(int(i), b2, b1, b0)
            else:
                b3 = int(i & 0x7F)
                self.write_bytes(int(i >> 7), b3, b2, b1, b0)

    def write_signed_vint(self, i: int) -> None:
        """
        Helper method for writing 32-bit signed value, using
        "zig zag encoding" (see protocol buffers for explanation -- basically,
        sign bit is moved as LSB, rest of value shifted left by one)
        coupled with basic variable length encoding
        :param i: Signed int
        """
        self.write_positive_vint(util.zigzag_encode(i))

    # Helper methods
    def _add_seen_name(self, name: Union[bytes, str]) -> None:
        if self.shared_keys:
            if len(self.shared_keys) == constants.MAX_SHARED_NAMES:
                self.shared_keys = [None] * len(self.shared_keys)
            else:
                old = copy.copy(self.shared_keys)
                self.shared_keys = [None] * constants.MAX_SHARED_NAMES
                mask = constants.MAX_SHARED_NAMES - 1
                for node in old:
                    while node:
                        ix = util.hash_string(node.value) & mask
                        next_node = node.next
                        try:
                            node.next = self.shared_keys[ix]
                        except IndexError:
                            node.next = None
                        self.shared_keys[ix] = node
                        node = next_node
            if _is_valid_back_ref(len(self.shared_keys)):
                ix = util.hash_string(name) & (len(self.shared_keys) - 1)
                self.shared_keys[ix] = SharedStringNode(name, self.shared_keys[ix])

    def _add_seen_string_value(self, text: str) -> None:
        if self.shared_values:
            if self.seen_string_count == constants.MAX_SHARED_STRING_VALUES:
                self.seen_string_count = 0
                self.shared_values = [None] * len(self.shared_values)
            else:
                old = copy.copy(self.shared_values)
                self.shared_values = [None] * constants.MAX_SHARED_STRING_VALUES
                mask = constants.MAX_SHARED_STRING_VALUES - 1
                for node in old:
                    while node:
                        ix = util.hash_string(node.value) & mask
                        next_node = node.next
                        try:
                            node.next = self.shared_values[ix]
                        except IndexError:
                            node.next = None
                        self.shared_values[ix] = node
                        node = next_node
            if _is_valid_back_ref(len(self.shared_values)):
                ix = util.hash_string(text) & (len(self.shared_values) - 1)
                self.shared_values[ix] = SharedStringNode(text, self.shared_values[ix])

    def _find_seen_name(self, name: Union[bytes, str]) -> int:
        n_hash = util.hash_string(name)
        try:
            head = self.shared_keys[n_hash & (len(self.shared_keys) - 1)]
        except IndexError:
            return -1
        if head is None:
            return -1

        if head.value is name:
            return head.index

        node = head
        while node:
            if node.value is name:
                return node.index
            node = node.next
        node = head
        while node:
            if node.value == name and util.hash_string(node.value) == n_hash:
                return node.index
            node = node.next

    def _find_seen_string_value(self, text: str) -> int:
        hash_ = util.hash_string(text)
        try:
            head = self.shared_values[hash_ & (len(self.shared_values) - 1)]
        except IndexError:
            return -1
        if head is None:
            return -1
        node = head
        while node:
            if node.value is text:
                return node.index
            node = node.next
        node = head
        while node:
            if util.hash_string(node.value) == hash_ and node.value == text:
                return node.index
            node = node.next

    # Actual encoding
    def _encode_array(self, arr: Union[list, tuple, set]) -> None:
        self.write_start_array()
        for idx in arr:
            self._iter_encode(idx)
        self.write_end_array()

    def _encode_dict(self, d: dict) -> None:
        self.write_start_object()
        for k, v in d.items():
            if k is None:
                k = "null"
            elif isinstance(k, bool):
                k = "true" if k else "false"
            elif isinstance(k, int):
                k = str(k)
            elif isinstance(k, float):
                k = self._floatstr(k)
            elif not isinstance(k, str):
                raise TypeError(f"Key {k} is not a string")
            self.write_field_name(k)
            self._iter_encode(v)
        self.write_end_object()

    def _floatstr(self, flt: float) -> str:
        """
        Convert a Python float into a JSON float string
        :param float flt: Floating point number
        :returns: JSON String representation of the float
        :rtype: str
        """
        _inf = float("inf")
        if flt != flt:
            return "NaN"
        if flt == _inf:
            return "Infinity"
        if flt == -_inf:
            return "-Infinity"
        return repr(flt)

    def _iter_encode(self, obj: Union[dict, list, set, tuple]) -> None:
        if encoder := self._encoders.get(type(obj), None):
            encoder(obj)
        else:
            self._iter_encode(obj)

    def encode(self, py_obj: Union[dict, list, set, tuple], header: bool = True, ender: bool = False) -> bytes:
        """
        SMILE Encode object
        :param dict|list|set|tuple py_obj: The object to be encoded
        :param bool header: (optional - Default: `True`)
        :param bool ender: (optional - Default: `False`)
        :returns: SMILE encoded data
        """
        if isinstance(py_obj, (set, tuple)):
            py_obj = list(py_obj)
        elif not isinstance(py_obj, (dict, list)):
            raise ValueError(f"Invalid type for 'obj' paramater. Must be one of dict, list, set, or tuple; given {type(py_obj)}")

        if header:
            self.write_header()

        self._iter_encode(py_obj)

        if ender:
            self.write_ender()
        return bytes(self.output)

    @classmethod
    def encode_obj(cls, py_obj: Union[list, dict], header: bool = True, ender: bool = False, shared_keys: bool = True, shared_vals: bool = True, bin_7bit: bool = True) -> bytes:
        """
        SMILE Encode object
        :param list|dict py_obj: The object to be encoded
        :param bool header: (optional - Default: `True`)
        :param bool ender: (optional - Default: `False`)
        :param bool bin_7bit: (optional - Default: `True`) Encode raw data as 7-bit
        :param bool shared_keys: (optional - Default: `True`) Shared Key String References
        :param bool shared_vals: (optional - Default: `True`) Shared Value String References
        :returns: SMILE encoded data
        """
        if isinstance(py_obj, (tuple, set)):
            py_obj = list(py_obj)
        elif not isinstance(py_obj, (list, dict)):
            raise ValueError("Invalid type for \"obj\" paramater.  Must be one of dict, list, set, or tuple")

        enc_obj = cls(shared_keys, shared_vals, bin_7bit)
        return enc_obj.encode(py_obj, header, ender)


def _is_valid_back_ref(index):
    """
    Helper method used to ensure that we do not use back-reference values
    that would produce illegal byte sequences (ones with byte 0xFE or 0xFF).
    Note that we do not try to avoid null byte (0x00) by default, although it would be technically possible as well.
    :param int index: Index
    :returns: Valid back ref
    :rtype: bool
    """
    return (index & 0xFF) < 0xFE


def encode(py_obj: Union[list, dict], header: bool = True, ender: bool = False, shared_keys: bool = True, shared_vals: bool = True, bin_7bit: bool = True) -> bytes:
    """
    SMILE Encode object
    :param dict|list|set|tuple py_obj: The object to be encoded
    :param bool header: (optional - Default: `True`)
    :param bool ender: (optional - Default: `False`)
    :param bool bin_7bit: (optional - Default: `True`) Encode raw data as 7-bit
    :param bool shared_keys: (optional - Default: `True`) Shared Key String References
    :param bool shared_vals: (optional - Default: `True`) Shared Value String References
    :returns: SMILE encoded data
    """
    return SmileEncoder.encode_obj(py_obj, header, ender, shared_keys, shared_vals, bin_7bit)
