"""Common types for encoder and decoder"""

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Data Formats
BINN_LIST = b'\xe0'
BINN_MAP = b'\xe1'
BINN_OBJECT = b'\xe2'

BINN_STRING = b'\xa0'
BINN_TIME = b'\xa1'  # Not used
BINN_DATETIME = b'\xa2'

BINN_BLOB = b'\xc0'

BINN_NULL = b'\x00'
BINN_TRUE = b'\x01'
BINN_FALSE = b'\x02'

BINN_UINT8 = b'\x20'
BINN_INT8 = b'\x21'
BINN_UINT16 = b'\x40'
BINN_INT16 = b'\x41'
BINN_UINT32 = b'\x60'
BINN_INT32 = b'\x61'
BINN_UINT64 = b'\x80'
BINN_INT64 = b'\x81'
BINN_FLOAT64 = b'\x82'

# Extended data formats
PYBINN_MAP = b'\xb8'
PYBINN_MAP_SIZE = 8

ALL = (
    BINN_LIST,
    BINN_MAP,
    BINN_OBJECT,
    BINN_STRING,
    BINN_DATETIME,
    BINN_BLOB,
    BINN_NULL,
    BINN_TRUE,
    BINN_FALSE,
    BINN_UINT8,
    BINN_INT8,
    BINN_UINT16,
    BINN_INT16,
    BINN_UINT32,
    BINN_INT32,
    BINN_UINT64,
    BINN_INT64,
    BINN_FLOAT64,
    PYBINN_MAP
)
