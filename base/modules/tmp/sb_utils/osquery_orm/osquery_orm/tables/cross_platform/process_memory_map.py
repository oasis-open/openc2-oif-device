"""
OSQuery process_memory_map ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class ProcessMemoryMap(BaseModel):
    """
    Process memory mapped files and pseudo device/regions.
    Examples:
        select * from process_memory_map where pid = 1
    """
    pid = IntegerField(help_text="Process (or thread) ID")  # {'index': True}
    start = TextField(help_text="Virtual start address (hex)")
    end = TextField(help_text="Virtual end address (hex)")
    permissions = TextField(help_text="r=read, w=write, x=execute, p=private (cow)")
    offset = BigIntegerField(help_text="Offset into mapped path")
    device = TextField(help_text="MA:MI Major/minor device ID")
    inode = IntegerField(help_text="Mapped path inode, 0 means uninitialized (BSS)")
    path = TextField(help_text="Path to mapped file or mapped type")
    pseudo = IntegerField(help_text="1 If path is a pseudo path, else 0")

    class Meta:
        table_name = "process_memory_map"
