"""
OSQuery syslog_events ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class SyslogEvents(BaseModel):
    time = BigIntegerField(help_text="Current unix epoch time")
    datetime = TextField(help_text="Time known to syslog")
    host = TextField(help_text="Hostname configured for syslog")
    severity = IntegerField(help_text="Syslog severity")
    facility = TextField(help_text="Syslog facility")
    tag = TextField(help_text="The syslog tag")
    message = TextField(help_text="The syslog message")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "syslog_events"
