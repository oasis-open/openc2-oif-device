"""
OSQuery disk_info ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DiskInfo(BaseModel):
    """
    Retrieve basic information about the physical disks of a system.
    """
    partitions = IntegerField(help_text="Number of detected partitions on disk.")
    disk_index = IntegerField(help_text="Physical drive number of the disk.")
    type = TextField(help_text="The interface type of the disk.")
    id = TextField(help_text="The unique identifier of the drive on the system.")
    pnp_device_id = TextField(help_text="The unique identifier of the drive on the system.")
    disk_size = BigIntegerField(help_text="Size of the disk.")
    manufacturer = TextField(help_text="The manufacturer of the disk.")
    hardware_model = TextField(help_text="Hard drive model.")
    name = TextField(help_text="The label of the disk object.")
    serial = TextField(help_text="The serial number of the disk.")
    description = TextField(help_text="The OS\'s description of the disk.")

    class Meta:
        table_name = "disk_info"
