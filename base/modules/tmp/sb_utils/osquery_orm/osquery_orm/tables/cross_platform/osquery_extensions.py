"""
OSQuery osquery_extensions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class OsqueryExtensions(BaseModel):
    """
    List of active osquery extensions.
    """
    uuid = BigIntegerField(help_text="The transient ID assigned for communication")
    name = TextField(help_text="Extension\'s name")
    version = TextField(help_text="Extension\'s version")
    sdk_version = TextField(help_text="osquery SDK version used to build the extension")
    path = TextField(help_text="Path of the extension\'s Thrift connection or library path")
    type = TextField(help_text="SDK extension type: extension or module")

    class Meta:
        table_name = "osquery_extensions"
