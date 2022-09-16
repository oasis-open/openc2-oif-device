"""
OSQuery scheduled_tasks ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class ScheduledTasks(BaseModel):
    """
    Lists all of the tasks in the Windows task scheduler.
    Examples:
        select * from scheduled_tasks
        select * from scheduled_tasks where hidden=1 and enabled=1
    """
    name = TextField(help_text="Name of the scheduled task")
    action = TextField(help_text="Actions executed by the scheduled task")
    path = TextField(help_text="Path to the executable to be run")
    enabled = IntegerField(help_text="Whether or not the scheduled task is enabled")
    state = TextField(help_text="State of the scheduled task")
    hidden = IntegerField(help_text="Whether or not the task is visible in the UI")
    last_run_time = BigIntegerField(help_text="Timestamp the task last ran")
    next_run_time = BigIntegerField(help_text="Timestamp the task is scheduled to run next")
    last_run_message = TextField(help_text="Exit status message of the last task run")
    last_run_code = TextField(help_text="Exit status code of the last task run")

    class Meta:
        table_name = "scheduled_tasks"
