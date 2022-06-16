"""
OSQuery oem_strings ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OemStrings(BaseModel):
    """
    OEM defined strings retrieved from SMBIOS.
    """
    handle = TextField(help_text="Handle, or instance number, associated with the Type 11 structure")
    number = IntegerField(help_text="The string index of the structure")
    value = TextField(help_text="The value of the OEM string")

    class Meta:
        table_name = "oem_strings"
