"""
OSQuery logical_drives ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class LogicalDrives(BaseModel):
    """
    Details for logical drives on the system. A logical drive generally represents a single partition.
    Examples:
        select * from logical_drives
        select free_space from logical_drives where device_id = 'C:'
    """
    device_id = TextField(help_text="The drive id, usually the drive name, e.g., \'C:\'.")
    type = TextField(help_text="Deprecated (always \'Unknown\').")
    description = TextField(help_text="The canonical description of the drive, e.g. \'Logical Fixed Disk\', \'CD-ROM Disk\'.")
    free_space = BigIntegerField(help_text="The amount of free space, in bytes, of the drive (-1 on failure).")
    size = BigIntegerField(help_text="The total amount of space, in bytes, of the drive (-1 on failure).")
    file_system = TextField(help_text="The file system of the drive.")
    boot_partition = IntegerField(help_text="True if Windows booted from this drive.")

    class Meta:
        table_name = "logical_drives"
