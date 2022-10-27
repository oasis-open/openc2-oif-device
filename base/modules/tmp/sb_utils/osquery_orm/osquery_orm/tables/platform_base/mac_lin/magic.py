"""
OSQuery magic ORM
"""
from ....orm import BaseModel
from peewee import TextField


class Magic(BaseModel):
    """
    Magic number recognition library table.
    """
    path = TextField(help_text="Absolute path to target file")  # {'required': True, 'index': True}
    magic_db_files = TextField(help_text="Colon(:) separated list of files where the magic db file can be found. By default one of the following is used: /usr/share/file/magic/magic, /usr/share/misc/magic or /usr/share/misc/magic.mgc")  # {'additional': True}
    data = TextField(help_text="Magic number data from libmagic")
    mime_type = TextField(help_text="MIME type data from libmagic")
    mime_encoding = TextField(help_text="MIME encoding data from libmagic")

    class Meta:
        table_name = "magic"
