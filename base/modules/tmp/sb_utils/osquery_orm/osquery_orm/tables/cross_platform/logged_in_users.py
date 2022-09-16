"""
OSQuery logged_in_users ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class LoggedInUsers(BaseModel):
    """
    Users with an active shell on the system.
    """
    type = TextField(help_text="Login type")
    user = TextField(help_text="User login name")
    tty = TextField(help_text="Device name")
    host = TextField(help_text="Remote hostname")
    time = BigIntegerField(help_text="Time entry was made")
    pid = IntegerField(help_text="Process (or thread) ID")

    class Meta:
        table_name = "logged_in_users"


# OS specific properties for Windows
class Windows_LoggedInUsers(LoggedInUsers):
    sid = TextField(help_text="The user\'s unique security identifier")
    registry_hive = TextField(help_text="HKEY_USERS registry hive")

    class Meta:
        table_name = "logged_in_users"
