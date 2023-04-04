"""
OSQuery md_drives ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class MdDrives(BaseModel):
    """
    Drive devices used for Software RAID.
    """
    md_device_name = TextField(help_text="md device name")
    drive_name = TextField(help_text="Drive device name")
    slot = IntegerField(help_text="Slot position of disk")
    state = TextField(help_text="State of the drive")

    class Meta:
        table_name = "md_drives"
