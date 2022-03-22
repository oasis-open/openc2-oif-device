"""
OSQuery disk_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DiskEvents(BaseModel):
    """
    Track DMG disk image events (appearance/disappearance) when opened.
    """
    action = TextField(help_text="Appear or disappear")
    path = TextField(help_text="Path of the DMG file accessed")
    name = TextField(help_text="Disk event name")
    device = TextField(help_text="Disk event BSD name")  # {'aliases': ['bsd_name']}
    uuid = TextField(help_text="UUID of the volume inside DMG if available")
    size = BigIntegerField(help_text="Size of partition in bytes")
    ejectable = IntegerField(help_text="1 if ejectable, 0 if not")
    mountable = IntegerField(help_text="1 if mountable, 0 if not")
    writable = IntegerField(help_text="1 if writable, 0 if not")
    content = TextField(help_text="Disk event content")
    media_name = TextField(help_text="Disk event media name string")
    vendor = TextField(help_text="Disk event vendor string")
    filesystem = TextField(help_text="Filesystem if available")
    checksum = TextField(help_text="UDIF Master checksum if available (CRC32)")
    time = BigIntegerField(help_text="Time of appearance/disappearance in UNIX time")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "disk_events"
