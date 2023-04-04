"""
OSQuery fbsd_kmods ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class FbsdKmods(BaseModel):
    """
    Loaded FreeBSD kernel modules.
    """
    name = TextField(help_text="Module name")
    size = IntegerField(help_text="Size of module content")
    refs = IntegerField(help_text="Module reverse dependencies")
    address = TextField(help_text="Kernel module address")

    class Meta:
        table_name = "fbsd_kmods"
