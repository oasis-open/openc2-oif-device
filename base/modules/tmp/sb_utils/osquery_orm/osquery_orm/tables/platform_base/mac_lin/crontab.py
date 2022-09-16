"""
OSQuery crontab ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class Crontab(BaseModel):
    """
    Line parsed values from system and user cron/tab.
    """
    event = TextField(help_text="The job @event name (rare)")
    minute = TextField(help_text="The exact minute for the job")
    hour = TextField(help_text="The hour of the day for the job")
    day_of_month = TextField(help_text="The day of the month for the job")
    month = TextField(help_text="The month of the year for the job")
    day_of_week = TextField(help_text="The day of the week for the job")
    command = TextField(help_text="Raw command string")
    path = TextField(help_text="File parsed")

    class Meta:
        table_name = "crontab"


# OS specific properties for Linux
class Linux_Crontab(Crontab):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "crontab"
