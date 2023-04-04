"""
OSQuery device_partitions ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DevicePartitions(BaseModel):
    """
    Use TSK to enumerate details about partitions on a disk device.
    """
    device = TextField(help_text="Absolute file path to device node")  # {'required': True}
    partition = IntegerField(help_text="A partition number or description")
    label = TextField(help_text="")
    type = TextField(help_text="")
    offset = BigIntegerField(help_text="")
    blocks_size = BigIntegerField(help_text="Byte size of each block")
    blocks = BigIntegerField(help_text="Number of blocks")
    inodes = BigIntegerField(help_text="Number of meta nodes")
    flags = IntegerField(help_text="")

    class Meta:
        table_name = "device_partitions"
