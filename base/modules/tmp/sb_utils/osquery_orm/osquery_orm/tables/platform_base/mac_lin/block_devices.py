"""
OSQuery block_devices ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class BlockDevices(BaseModel):
    """
    Block (buffered access) device file nodes: disks, ramdisks, and DMG containers.
    """
    name = TextField(help_text="Block device name")
    parent = TextField(help_text="Block device parent name")
    vendor = TextField(help_text="Block device vendor string")
    model = TextField(help_text="Block device model string identifier")
    size = BigIntegerField(help_text="Block device size in blocks")
    block_size = IntegerField(help_text="Block size in bytes")
    uuid = TextField(help_text="Block device Universally Unique Identifier")
    type = TextField(help_text="Block device type string")
    label = TextField(help_text="Block device label string")

    class Meta:
        table_name = "block_devices"
