"""
OSQuery user_events ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class UserEvents(BaseModel):
    """
    Track user events from the audit framework.
    """
    uid = BigIntegerField(help_text="User ID")
    auid = BigIntegerField(help_text="Audit User ID")
    pid = BigIntegerField(help_text="Process (or thread) ID")
    message = TextField(help_text="Message from the event")
    type = IntegerField(help_text="The file description for the process socket")
    path = TextField(help_text="Supplied path from event")
    address = TextField(help_text="The Internet protocol address or family ID")
    terminal = TextField(help_text="The network protocol ID")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "user_events"
