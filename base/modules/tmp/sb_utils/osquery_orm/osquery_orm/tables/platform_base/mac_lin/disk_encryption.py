"""
OSQuery disk_encryption ORM
"""
from ....orm import BaseModel
from peewee import ForeignKeyField, IntegerField, TextField
from .block_devices import BlockDevices


class DiskEncryption(BaseModel):
    """
    Disk encryption status and information.
    """
    name = TextField(help_text="Disk name")  # {'index': True}
    uuid = TextField(help_text="Disk Universally Unique Identifier")
    encrypted = IntegerField(help_text="1 If encrypted: true (disk is encrypted), else 0")
    type = TextField(help_text="Description of cipher type and mode if available")
    encryption_status = TextField(help_text="Disk encryption status with one of following values: encrypted | not encrypted | undefined")
    disk_encryption = ForeignKeyField(BlockDevices, backref='name')
    disk_encryption = ForeignKeyField(BlockDevices, backref='uuid')

    class Meta:
        table_name = "disk_encryption"


# OS specific properties for MacOS
class MacOS_DiskEncryption(DiskEncryption):
    uid = TextField(help_text="Currently authenticated user if available")
    user_uuid = TextField(help_text="UUID of authenticated user if available")
    filevault_status = TextField(help_text="FileVault status with one of following values: on | off | unknown")

    class Meta:
        table_name = "disk_encryption"
