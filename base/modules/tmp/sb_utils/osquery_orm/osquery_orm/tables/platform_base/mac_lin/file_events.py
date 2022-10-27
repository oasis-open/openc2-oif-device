"""
OSQuery file_events ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class FileEvents(BaseModel):
    """
    Track time/action changes to files specified in configuration data.
    """
    target_path = TextField(help_text="The path associated with the event")
    category = TextField(help_text="The category of the file defined in the config")
    action = TextField(help_text="Change action (UPDATE, REMOVE, etc)")
    transaction_id = BigIntegerField(help_text="ID used during bulk update")
    inode = BigIntegerField(help_text="Filesystem inode number")
    uid = BigIntegerField(help_text="Owning user ID")
    gid = BigIntegerField(help_text="Owning group ID")
    mode = TextField(help_text="Permission bits")
    size = BigIntegerField(help_text="Size of file in bytes")
    atime = BigIntegerField(help_text="Last access time")
    mtime = BigIntegerField(help_text="Last modification time")
    ctime = BigIntegerField(help_text="Last status change time")
    md5 = TextField(help_text="The MD5 of the file after change")
    sha1 = TextField(help_text="The SHA1 of the file after change")
    sha256 = TextField(help_text="The SHA256 of the file after change")
    hashed = IntegerField(help_text="1 if the file was hashed, 0 if not, -1 if hashing failed")
    time = BigIntegerField(help_text="Time of file event")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "file_events"
