"""
OSQuery xprotect_meta ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class XprotectMeta(BaseModel):
    """
    Database of the machine\'s XProtect browser-related signatures.
    """
    identifier = TextField(help_text="Browser plugin or extension identifier")
    type = TextField(help_text="Either plugin or extension")
    developer_id = TextField(help_text="Developer identity (SHA1) of extension")
    min_version = TextField(help_text="The minimum allowed plugin version.")

    class Meta:
        table_name = "xprotect_meta"
