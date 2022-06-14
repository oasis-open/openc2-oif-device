"""
OSQuery md_devices ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class MdDevices(BaseModel):
    """
    Software RAID array settings.
    """
    device_name = TextField(help_text="md device name")
    status = TextField(help_text="Current state of the array")
    raid_level = IntegerField(help_text="Current raid level of the array")
    size = BigIntegerField(help_text="size of the array in blocks")
    chunk_size = BigIntegerField(help_text="chunk size in bytes")
    raid_disks = IntegerField(help_text="Number of configured RAID disks in array")
    nr_raid_disks = IntegerField(help_text="Number of partitions or disk devices to comprise the array")
    working_disks = IntegerField(help_text="Number of working disks in array")
    active_disks = IntegerField(help_text="Number of active disks in array")
    failed_disks = IntegerField(help_text="Number of failed disks in array")
    spare_disks = IntegerField(help_text="Number of idle disks in array")
    superblock_state = TextField(help_text="State of the superblock")
    superblock_version = TextField(help_text="Version of the superblock")
    superblock_update_time = BigIntegerField(help_text="Unix timestamp of last update")
    bitmap_on_mem = TextField(help_text="Pages allocated in in-memory bitmap, if enabled")
    bitmap_chunk_size = TextField(help_text="Bitmap chunk size")
    bitmap_external_file = TextField(help_text="External referenced bitmap file")
    recovery_progress = TextField(help_text="Progress of the recovery activity")
    recovery_finish = TextField(help_text="Estimated duration of recovery activity")
    recovery_speed = TextField(help_text="Speed of recovery activity")
    resync_progress = TextField(help_text="Progress of the resync activity")
    resync_finish = TextField(help_text="Estimated duration of resync activity")
    resync_speed = TextField(help_text="Speed of resync activity")
    reshape_progress = TextField(help_text="Progress of the reshape activity")
    reshape_finish = TextField(help_text="Estimated duration of reshape activity")
    reshape_speed = TextField(help_text="Speed of reshape activity")
    check_array_progress = TextField(help_text="Progress of the check array activity")
    check_array_finish = TextField(help_text="Estimated duration of the check array activity")
    check_array_speed = TextField(help_text="Speed of the check array activity")
    unused_devices = TextField(help_text="Unused devices")
    other = TextField(help_text="Other information associated with array from /proc/mdstat")

    class Meta:
        table_name = "md_devices"
