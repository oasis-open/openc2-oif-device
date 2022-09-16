"""
OSQuery shared_memory ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class SharedMemory(BaseModel):
    """
    OS shared memory regions.
    """
    shmid = IntegerField(help_text="Shared memory segment ID")
    owner_uid = BigIntegerField(help_text="User ID of owning process")
    creator_uid = BigIntegerField(help_text="User ID of creator process")
    pid = BigIntegerField(help_text="Process ID to last use the segment")
    creator_pid = BigIntegerField(help_text="Process ID that created the segment")
    atime = BigIntegerField(help_text="Attached time")
    dtime = BigIntegerField(help_text="Detached time")
    ctime = BigIntegerField(help_text="Changed time")
    permissions = TextField(help_text="Memory segment permissions")
    size = BigIntegerField(help_text="Size in bytes")
    attached = IntegerField(help_text="Number of attached processes")
    status = TextField(help_text="Destination/attach status")
    locked = IntegerField(help_text="1 if segment is locked else 0")

    class Meta:
        table_name = "shared_memory"
