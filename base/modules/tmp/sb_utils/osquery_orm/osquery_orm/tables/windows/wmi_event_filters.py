"""
OSQuery wmi_event_filters ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class WmiEventFilters(BaseModel):
    """
    Lists WMI event filters.
    Examples:
        select * from wmi_event_filters
    """
    name = TextField(help_text="Unique identifier of an event filter.")
    query = TextField(help_text="Windows Management Instrumentation Query Language (WQL) event query that specifies the set of events for consumer notification, and the specific conditions for notification.")
    query_language = TextField(help_text="Query language that the query is written in.")
    class_ = TextField(help_text="The name of the class.", column_name="class")
    relative_path = TextField(help_text="Relative path to the class or instance.")

    class Meta:
        table_name = "wmi_event_filters"
