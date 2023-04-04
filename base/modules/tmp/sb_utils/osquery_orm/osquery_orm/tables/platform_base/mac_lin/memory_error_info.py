"""
OSQuery memory_error_info ORM
"""
from ....orm import BaseModel
from peewee import TextField


class MemoryErrorInfo(BaseModel):
    """
    Data associated with errors of a physical memory array.
    """
    handle = TextField(help_text="Handle, or instance number, associated with the structure")
    error_type = TextField(help_text="type of error associated with current error status for array or device")
    error_granularity = TextField(help_text="Granularity to which the error can be resolved")
    error_operation = TextField(help_text="Memory access operation that caused the error")
    vendor_syndrome = TextField(help_text="Vendor specific ECC syndrome or CRC data associated with the erroneous access")
    memory_array_error_address = TextField(help_text="32 bit physical address of the error based on the addressing of the bus to which the memory array is connected")
    device_error_address = TextField(help_text="32 bit physical address of the error relative to the start of the failing memory address, in bytes")
    error_resolution = TextField(help_text="Range, in bytes, within which this error can be determined, when an error address is given")

    class Meta:
        table_name = "memory_error_info"
