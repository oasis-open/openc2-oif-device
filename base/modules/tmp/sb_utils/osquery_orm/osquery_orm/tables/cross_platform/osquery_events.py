"""
OSQuery osquery_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OsqueryEvents(BaseModel):
    """
    Information about the event publishers and subscribers.
    """
    name = TextField(help_text="Event publisher or subscriber name")
    publisher = TextField(help_text="Name of the associated publisher")
    type = TextField(help_text="Either publisher or subscriber")
    subscriptions = IntegerField(help_text="Number of subscriptions the publisher received or subscriber used")
    events = IntegerField(help_text="Number of events emitted or received since osquery started")
    refreshes = IntegerField(help_text="Publisher only: number of runloop restarts")
    active = IntegerField(help_text="1 if the publisher or subscriber is active else 0")

    class Meta:
        table_name = "osquery_events"
