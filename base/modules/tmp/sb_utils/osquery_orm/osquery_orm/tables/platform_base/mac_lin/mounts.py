"""
OSQuery mounts ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class Mounts(BaseModel):
    """
    System mounted devices and filesystems (not process specific).
    """
    device = TextField(help_text="Mounted device")
    device_alias = TextField(help_text="Mounted device alias")
    path = TextField(help_text="Mounted device path")
    type = TextField(help_text="Mounted device type")
    blocks_size = BigIntegerField(help_text="Block size in bytes")
    blocks = BigIntegerField(help_text="Mounted device used blocks")
    blocks_free = BigIntegerField(help_text="Mounted device free blocks")
    blocks_available = BigIntegerField(help_text="Mounted device available blocks")
    inodes = BigIntegerField(help_text="Mounted device used inodes")
    inodes_free = BigIntegerField(help_text="Mounted device free inodes")
    flags = TextField(help_text="Mounted device flags")

    class Meta:
        table_name = "mounts"
