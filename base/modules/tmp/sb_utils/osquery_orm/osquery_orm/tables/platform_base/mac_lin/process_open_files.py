"""
OSQuery process_open_files ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class ProcessOpenFiles(BaseModel):
    """
    File descriptors for each process.
    Examples:
        select * from process_open_files where pid = 1
    """
    pid = BigIntegerField(help_text="Process (or thread) ID")  # {'index': True}
    fd = BigIntegerField(help_text="Process-specific file descriptor number")
    path = TextField(help_text="Filesystem path of descriptor")

    class Meta:
        table_name = "process_open_files"
