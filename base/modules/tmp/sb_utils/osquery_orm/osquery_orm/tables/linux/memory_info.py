"""
OSQuery memory_info ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField


class MemoryInfo(BaseModel):
    """
    Main memory information in bytes.
    """
    memory_total = BigIntegerField(help_text="Total amount of physical RAM, in bytes")
    memory_free = BigIntegerField(help_text="The amount of physical RAM, in bytes, left unused by the system")
    buffers = BigIntegerField(help_text="The amount of physical RAM, in bytes, used for file buffers")
    cached = BigIntegerField(help_text="The amount of physical RAM, in bytes, used as cache memory")
    swap_cached = BigIntegerField(help_text="The amount of swap, in bytes, used as cache memory")
    active = BigIntegerField(help_text="The total amount of buffer or page cache memory, in bytes, that is in active use")
    inactive = BigIntegerField(help_text="The total amount of buffer or page cache memory, in bytes, that are free and available")
    swap_total = BigIntegerField(help_text="The total amount of swap available, in bytes")
    swap_free = BigIntegerField(help_text="The total amount of swap free, in bytes")

    class Meta:
        table_name = "memory_info"
