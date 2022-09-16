"""
OSQuery md_personalities ORM
"""
from ...orm import BaseModel
from peewee import TextField


class MdPersonalities(BaseModel):
    """
    Software RAID setting supported by the kernel.
    """
    name = TextField(help_text="Name of personality supported by kernel")

    class Meta:
        table_name = "md_personalities"
