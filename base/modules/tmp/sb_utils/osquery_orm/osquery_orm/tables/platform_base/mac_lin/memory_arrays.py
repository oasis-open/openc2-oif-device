"""
OSQuery memory_arrays ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class MemoryArrays(BaseModel):
    """
    Data associated with collection of memory devices that operate to form a memory address.
    """
    handle = TextField(help_text="Handle, or instance number, associated with the array")
    location = TextField(help_text="Physical location of the memory array")
    use = TextField(help_text="Function for which the array is used")
    memory_error_correction = TextField(help_text="Primary hardware error correction or detection method supported")
    max_capacity = IntegerField(help_text="Maximum capacity of array in gigabytes")
    memory_error_info_handle = TextField(help_text="Handle, or instance number, associated with any error that was detected for the array")
    number_memory_devices = IntegerField(help_text="Number of memory devices on array")

    class Meta:
        table_name = "memory_arrays"
