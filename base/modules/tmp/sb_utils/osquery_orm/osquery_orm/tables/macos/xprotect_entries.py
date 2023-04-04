"""
OSQuery xprotect_entries ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class XprotectEntries(BaseModel):
    """
    Database of the machine\'s XProtect signatures.
    """
    name = TextField(help_text="Description of XProtected malware")
    launch_type = TextField(help_text="Launch services content type")
    identity = TextField(help_text="XProtect identity (SHA1) of content")
    filename = TextField(help_text="Use this file name to match")
    filetype = TextField(help_text="Use this file type to match")
    optional = IntegerField(help_text="Match any of the identities/patterns for this XProtect name")
    uses_pattern = IntegerField(help_text="Uses a match pattern instead of identity")

    class Meta:
        table_name = "xprotect_entries"
