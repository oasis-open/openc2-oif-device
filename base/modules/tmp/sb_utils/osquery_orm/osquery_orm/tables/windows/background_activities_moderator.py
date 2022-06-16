"""
OSQuery background_activities_moderator ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class BackgroundActivitiesModerator(BaseModel):
    """
    Background Activities Moderator (BAM) tracks application execution.
    Examples:
        select * from background_activities_moderator;
    """
    path = TextField(help_text="Application file path.")
    last_execution_time = BigIntegerField(help_text="Most recent time application was executed.")
    sid = TextField(help_text="User SID.")

    class Meta:
        table_name = "background_activities_moderator"
