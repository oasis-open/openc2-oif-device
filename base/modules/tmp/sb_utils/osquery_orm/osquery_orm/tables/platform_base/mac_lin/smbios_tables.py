"""
OSQuery smbios_tables ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class SmbiosTables(BaseModel):
    """
    BIOS (DMI) structure common details and content.
    """
    number = IntegerField(help_text="Table entry number")
    type = IntegerField(help_text="Table entry type")
    description = TextField(help_text="Table entry description")
    handle = IntegerField(help_text="Table entry handle")
    header_size = IntegerField(help_text="Header size in bytes")
    size = IntegerField(help_text="Table entry size in bytes")
    md5 = TextField(help_text="MD5 hash of table entry")

    class Meta:
        table_name = "smbios_tables"
