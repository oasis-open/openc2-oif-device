"""
OSQuery wmi_filter_consumer_binding ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class WmiFilterConsumerBinding(BaseModel):
    """
    Lists the relationship between event consumers and filters.
    Examples:
        select * from wmi_filter_consumer_binding
    """
    consumer = TextField(help_text="Reference to an instance of __EventConsumer that represents the object path to a logical consumer, the recipient of an event.")
    filter = TextField(help_text="Reference to an instance of __EventFilter that represents the object path to an event filter which is a query that specifies the type of event to be received.")
    class_ = TextField(help_text="The name of the class.", column_name="class")
    relative_path = TextField(help_text="Relative path to the class or instance.")

    class Meta:
        table_name = "wmi_filter_consumer_binding"
