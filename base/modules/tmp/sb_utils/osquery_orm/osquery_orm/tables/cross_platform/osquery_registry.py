"""
OSQuery osquery_registry ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OsqueryRegistry(BaseModel):
    """
    List the osquery registry plugins.
    """
    registry = TextField(help_text="Name of the osquery registry")
    name = TextField(help_text="Name of the plugin item")
    owner_uuid = IntegerField(help_text="Extension route UUID (0 for core)")
    internal = IntegerField(help_text="1 If the plugin is internal else 0")
    active = IntegerField(help_text="1 If this plugin is active else 0")

    class Meta:
        table_name = "osquery_registry"
