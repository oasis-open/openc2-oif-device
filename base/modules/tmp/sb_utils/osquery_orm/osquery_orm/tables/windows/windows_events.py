"""
OSQuery windows_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class WindowsEvents(BaseModel):
    """
    Windows Event logs.
    Examples:
        select * from windows_events where eventid=4104 and source='Security'
    """
    time = BigIntegerField(help_text="Timestamp the event was received")
    datetime = TextField(help_text="System time at which the event occurred")
    source = TextField(help_text="Source or channel of the event")
    provider_name = TextField(help_text="Provider name of the event")
    provider_guid = TextField(help_text="Provider guid of the event")
    computer_name = TextField(help_text="Hostname of system where event was generated")
    eventid = IntegerField(help_text="Event ID of the event")
    task = IntegerField(help_text="Task value associated with the event")
    level = IntegerField(help_text="The severity level associated with the event")
    keywords = TextField(help_text="A bitmask of the keywords defined in the event")
    data = TextField(help_text="Data associated with the event")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "windows_events"
