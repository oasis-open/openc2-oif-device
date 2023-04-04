"""
OSQuery lxd_storage_pools ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class LxdStoragePools(BaseModel):
    """
    LXD storage pool information.
    Examples:
        select * from lxd_storage_pools
    """
    name = TextField(help_text="Name of the storage pool")
    driver = TextField(help_text="Storage driver")
    source = TextField(help_text="Storage pool source")
    size = TextField(help_text="Size of the storage pool")
    space_used = BigIntegerField(help_text="Storage space used in bytes")
    space_total = BigIntegerField(help_text="Total available storage space in bytes for this storage pool")
    inodes_used = BigIntegerField(help_text="Number of inodes used")
    inodes_total = BigIntegerField(help_text="Total number of inodes available in this storage pool")

    class Meta:
        table_name = "lxd_storage_pools"
