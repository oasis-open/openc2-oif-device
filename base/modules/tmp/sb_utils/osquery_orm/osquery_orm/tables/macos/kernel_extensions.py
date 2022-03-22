"""
OSQuery kernel_extensions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class KernelExtensions(BaseModel):
    """
    OS X\'s kernel extensions, both loaded and within the load search path.
    """
    idx = IntegerField(help_text="Extension load tag or index")
    refs = IntegerField(help_text="Reference count")
    size = BigIntegerField(help_text="Bytes of wired memory used by extension")
    name = TextField(help_text="Extension label")
    version = TextField(help_text="Extension version")
    linked_against = TextField(help_text="Indexes of extensions this extension is linked against")
    path = TextField(help_text="Optional path to extension bundle")

    class Meta:
        table_name = "kernel_extensions"
