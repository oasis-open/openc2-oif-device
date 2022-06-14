"""
OSQuery office_mru ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class OfficeMru(BaseModel):
    """
    View recently opened Office documents.
    Examples:
        select * from office_mru;
    """
    application = TextField(help_text="Associated Office application")
    version = TextField(help_text="Office application version number")
    path = TextField(help_text="File path")
    last_opened_time = BigIntegerField(help_text="Most recent opened time file was opened")
    sid = TextField(help_text="User SID")

    class Meta:
        table_name = "office_mru"
