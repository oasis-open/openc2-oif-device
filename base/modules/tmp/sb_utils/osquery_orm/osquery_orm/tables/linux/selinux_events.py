"""
OSQuery selinux_events ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class SelinuxEvents(BaseModel):
    """
    Track SELinux events.
    """
    type = TextField(help_text="Event type")
    message = TextField(help_text="Message")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "selinux_events"
