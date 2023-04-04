"""
OSQuery ie_extensions ORM
"""
from ...orm import BaseModel
from peewee import TextField


class IeExtensions(BaseModel):
    """
    Internet Explorer browser extensions.
    """
    name = TextField(help_text="Extension display name")
    registry_path = TextField(help_text="Extension identifier")
    version = TextField(help_text="Version of the executable")
    path = TextField(help_text="Path to executable")

    class Meta:
        table_name = "ie_extensions"
