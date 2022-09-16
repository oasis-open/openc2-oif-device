"""
OSQuery memory_map ORM
"""
from ...orm import BaseModel
from peewee import TextField


class MemoryMap(BaseModel):
    """
    OS memory region map.
    """
    name = TextField(help_text="Region name")
    start = TextField(help_text="Start address of memory region")
    end = TextField(help_text="End address of memory region")

    class Meta:
        table_name = "memory_map"
