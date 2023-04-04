"""
OSQuery device_hash ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class DeviceHash(BaseModel):
    """
    Similar to the hash table, but use TSK and allow block address access.
    """
    device = TextField(help_text="Absolute file path to device node")  # {'required': True}
    partition = TextField(help_text="A partition number")  # {'required': True}
    inode = BigIntegerField(help_text="Filesystem inode number")  # {'required': True}
    md5 = TextField(help_text="MD5 hash of provided inode data")
    sha1 = TextField(help_text="SHA1 hash of provided inode data")
    sha256 = TextField(help_text="SHA256 hash of provided inode data")

    class Meta:
        table_name = "device_hash"
