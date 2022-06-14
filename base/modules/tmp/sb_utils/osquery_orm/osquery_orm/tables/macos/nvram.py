"""
OSQuery nvram ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Nvram(BaseModel):
    """
    Apple NVRAM variable listing.
    """
    name = TextField(help_text="Variable name")  # {'additional': True, 'index': True}
    type = TextField(help_text="Data type (CFData, CFString, etc)")
    value = TextField(help_text="Raw variable data")

    class Meta:
        table_name = "nvram"
