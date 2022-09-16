"""
OSQuery time ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Time(BaseModel):
    """
    Track current date and time in UTC.
    """
    weekday = TextField(help_text="Current weekday in UTC")
    year = IntegerField(help_text="Current year in UTC")
    month = IntegerField(help_text="Current month in UTC")
    day = IntegerField(help_text="Current day in UTC")
    hour = IntegerField(help_text="Current hour in UTC")
    minutes = IntegerField(help_text="Current minutes in UTC")
    seconds = IntegerField(help_text="Current seconds in UTC")
    timezone = TextField(help_text="Timezone for reported time (hardcoded to UTC)")
    local_timezone = TextField(help_text="Current local timezone in of the system")
    unix_time = IntegerField(help_text="Current UNIX time in UTC")
    timestamp = TextField(help_text="Current timestamp (log format) in UTC")
    datetime = TextField(help_text="Current date and time (ISO format) in UTC")  # {'aliases': ['date_time']}
    iso_8601 = TextField(help_text="Current time (ISO format) in UTC")

    class Meta:
        table_name = "time"


# OS specific properties for Windows
class Windows_Time(Time):
    win_timestamp = BigIntegerField(help_text="Timestamp value in 100 nanosecond units")

    class Meta:
        table_name = "time"
