"""
OSQuery device_file ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DeviceFile(BaseModel):
    """
    Similar to the file table, but use TSK and allow block address access.
    """
    device = TextField(help_text="Absolute file path to device node")  # {'index': True, 'required': True}
    partition = TextField(help_text="A partition number")  # {'index': True, 'required': True}
    path = TextField(help_text="A logical path within the device node")  # {'additional': True}
    filename = TextField(help_text="Name portion of file path")
    inode = BigIntegerField(help_text="Filesystem inode number")  # {'index': True}
    uid = BigIntegerField(help_text="Owning user ID")
    gid = BigIntegerField(help_text="Owning group ID")
    mode = TextField(help_text="Permission bits")
    size = BigIntegerField(help_text="Size of file in bytes")
    block_size = IntegerField(help_text="Block size of filesystem")
    atime = BigIntegerField(help_text="Last access time")
    mtime = BigIntegerField(help_text="Last modification time")
    ctime = BigIntegerField(help_text="Creation time")
    hard_links = IntegerField(help_text="Number of hard links")
    type = TextField(help_text="File status")

    class Meta:
        table_name = "device_file"
