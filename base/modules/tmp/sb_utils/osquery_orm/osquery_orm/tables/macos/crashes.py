"""
OSQuery crashes ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Crashes(BaseModel):
    """
    Application, System, and Mobile App crash logs.
    Examples:
        select * from users join crashes using (uid)
    """
    type = TextField(help_text="Type of crash log")
    pid = BigIntegerField(help_text="Process (or thread) ID of the crashed process")
    path = TextField(help_text="Path to the crashed process")
    crash_path = TextField(help_text="Location of log file")  # {'index': True}
    identifier = TextField(help_text="Identifier of the crashed process")
    version = TextField(help_text="Version info of the crashed process")
    parent = BigIntegerField(help_text="Parent PID of the crashed process")
    responsible = TextField(help_text="Process responsible for the crashed process")
    uid = IntegerField(help_text="User ID of the crashed process")  # {'index': True}
    datetime = TextField(help_text="Date/Time at which the crash occurred")
    crashed_thread = BigIntegerField(help_text="Thread ID which crashed")
    stack_trace = TextField(help_text="Most recent frame from the stack trace")
    exception_type = TextField(help_text="Exception type of the crash")
    exception_codes = TextField(help_text="Exception codes from the crash")
    exception_notes = TextField(help_text="Exception notes from the crash")
    registers = TextField(help_text="The value of the system registers")

    class Meta:
        table_name = "crashes"
