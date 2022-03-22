"""
OSQuery asl ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Asl(BaseModel):
    """
    Queries the Apple System Log data structure for system events.
    """
    time = IntegerField(help_text="Unix timestamp.  Set automatically")  # {'additional': True}
    time_nano_sec = IntegerField(help_text="Nanosecond time.")  # {'additional': True}
    host = TextField(help_text="Sender\'s address (set by the server).")  # {'additional': True}
    sender = TextField(help_text="Sender\'s identification string.  Default is process name.")  # {'additional': True}
    facility = TextField(help_text="Sender\'s facility.  Default is \'user\'.")  # {'additional': True}
    pid = IntegerField(help_text="Sending process ID encoded as a string.  Set automatically.")  # {'additional': True}
    gid = BigIntegerField(help_text="GID that sent the log message (set by the server).")  # {'additional': True}
    uid = BigIntegerField(help_text="UID that sent the log message (set by the server).")  # {'additional': True}
    level = IntegerField(help_text="Log level number.  See levels in asl.h.")  # {'additional': True}
    message = TextField(help_text="Message text.")  # {'additional': True}
    ref_pid = IntegerField(help_text="Reference PID for messages proxied by launchd")  # {'additional': True}
    ref_proc = TextField(help_text="Reference process for messages proxied by launchd")  # {'additional': True}
    extra = TextField(help_text="Extra columns, in JSON format. Queries against this column are performed entirely in SQLite, so do not benefit from efficient querying via asl.h.")

    class Meta:
        table_name = "asl"
