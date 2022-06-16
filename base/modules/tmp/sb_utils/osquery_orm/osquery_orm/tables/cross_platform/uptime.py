"""
OSQuery uptime ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField


class Uptime(BaseModel):
    """
    Track time passed since last boot. Some systems track this as calendar time, some as runtime.
    """
    days = IntegerField(help_text="Days of uptime")
    hours = IntegerField(help_text="Hours of uptime")
    minutes = IntegerField(help_text="Minutes of uptime")
    seconds = IntegerField(help_text="Seconds of uptime")
    total_seconds = BigIntegerField(help_text="Total uptime seconds")

    class Meta:
        table_name = "uptime"
