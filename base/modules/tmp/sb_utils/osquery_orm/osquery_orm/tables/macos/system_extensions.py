"""
OSQuery system_extensions ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class SystemExtensions(BaseModel):
    """
    macOS (>= 10.15) system extension table.
    Examples:
        select * from system_extensions
    """
    path = TextField(help_text="Original path of system extension")
    UUID = TextField(help_text="Extension unique id")
    state = TextField(help_text="System extension state")
    identifier = TextField(help_text="Identifier name")
    version = TextField(help_text="System extension version")
    category = TextField(help_text="System extension category")
    bundle_path = TextField(help_text="System extension bundle path")
    team = TextField(help_text="Signing team ID")
    mdm_managed = IntegerField(help_text="1 if managed by MDM system extension payload configuration, 0 otherwise")

    class Meta:
        table_name = "system_extensions"
