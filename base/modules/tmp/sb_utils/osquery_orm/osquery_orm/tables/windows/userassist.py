"""
OSQuery userassist ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Userassist(BaseModel):
    """
    UserAssist Registry Key tracks when a user executes an application from Windows Explorer.
    Examples:
        select * from userassist;
    """
    path = TextField(help_text="Application file path.")
    last_execution_time = BigIntegerField(help_text="Most recent time application was executed.")
    count = IntegerField(help_text="Number of times the application has been executed.")
    sid = TextField(help_text="User SID.")

    class Meta:
        table_name = "userassist"
