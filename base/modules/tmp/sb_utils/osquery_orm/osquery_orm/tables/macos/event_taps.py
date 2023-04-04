"""
OSQuery event_taps ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class EventTaps(BaseModel):
    """
    Returns information about installed event taps.
    """
    enabled = IntegerField(help_text="Is the Event Tap enabled")
    event_tap_id = IntegerField(help_text="Unique ID for the Tap")
    event_tapped = TextField(help_text="The mask that identifies the set of events to be observed.")
    process_being_tapped = IntegerField(help_text="The process ID of the target application")
    tapping_process = IntegerField(help_text="The process ID of the application that created the event tap.")

    class Meta:
        table_name = "event_taps"
