"""
OSQuery time ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Time(BaseModel):
    """
    Track current date and time in the system.
    """
    weekday = TextField(help_text="Current weekday in the system")
    year = IntegerField(help_text="Current year in the system")
    month = IntegerField(help_text="Current month in the system")
    day = IntegerField(help_text="Current day in the system")
    hour = IntegerField(help_text="Current hour in the system")
    minutes = IntegerField(help_text="Current minutes in the system")
    seconds = IntegerField(help_text="Current seconds in the system")
    timezone = TextField(help_text="Current timezone in the system")
    local_time = IntegerField(help_text="Current local UNIX time in the system")  # {'aliases': ['localtime']}
    local_timezone = TextField(help_text="Current local timezone in the system")
    unix_time = IntegerField(help_text="Current UNIX time in the system, converted to UTC if --utc enabled")
    timestamp = TextField(help_text="Current timestamp (log format) in the system")
    datetime = TextField(help_text="Current date and time (ISO format) in the system")  # {'aliases': ['date_time']}
    iso_8601 = TextField(help_text="Current time (ISO format) in the system")

    class Meta:
        table_name = "time"


# OS specific properties for Windows
class Windows_Time(Time):
    win_timestamp = BigIntegerField(help_text="Timestamp value in 100 nanosecond units.")

    class Meta:
        table_name = "time"
