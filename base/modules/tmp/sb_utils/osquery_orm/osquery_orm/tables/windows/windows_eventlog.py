"""
OSQuery windows_eventlog ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class WindowsEventlog(BaseModel):
    """
    Table for querying all recorded Windows event logs.
    Examples:
        select * from windows_eventlog where eventid=4625 and channel='Security'
    """
    channel = TextField(help_text="Source or channel of the event")  # {'required': True}
    datetime = TextField(help_text="System time at which the event occurred")
    task = IntegerField(help_text="Task value associated with the event")
    level = IntegerField(help_text="Severity level associated with the event")
    provider_name = TextField(help_text="Provider name of the event")
    provider_guid = TextField(help_text="Provider guid of the event")
    computer_name = TextField(help_text="Hostname of system where event was generated")
    eventid = IntegerField(help_text="Event ID of the event")  # {'additional': True}
    keywords = TextField(help_text="A bitmask of the keywords defined in the event")
    data = TextField(help_text="Data associated with the event")
    pid = IntegerField(help_text="Process ID which emitted the event record")  # {'additional': True}
    tid = IntegerField(help_text="Thread ID which emitted the event record")
    time_range = TextField(help_text="System time to selectively filter the events")  # {'hidden': True, 'additional': True}
    timestamp = TextField(help_text="Timestamp to selectively filter the events")  # {'hidden': True, 'additional': True}
    xpath = TextField(help_text="The custom query to filter events")  # {'hidden': True, 'required': True}

    class Meta:
        table_name = "windows_eventlog"
