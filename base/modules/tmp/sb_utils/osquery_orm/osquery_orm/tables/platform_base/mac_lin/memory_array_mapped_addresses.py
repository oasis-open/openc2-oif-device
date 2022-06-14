"""
OSQuery memory_array_mapped_addresses ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class MemoryArrayMappedAddresses(BaseModel):
    """
    Data associated for address mapping of physical memory arrays.
    """
    handle = TextField(help_text="Handle, or instance number, associated with the structure")
    memory_array_handle = TextField(help_text="Handle of the memory array associated with this structure")
    starting_address = TextField(help_text="Physical stating address, in kilobytes, of a range of memory mapped to physical memory array")
    ending_address = TextField(help_text="Physical ending address of last kilobyte of a range of memory mapped to physical memory array")
    partition_width = IntegerField(help_text="Number of memory devices that form a single row of memory for the address partition of this structure")

    class Meta:
        table_name = "memory_array_mapped_addresses"
