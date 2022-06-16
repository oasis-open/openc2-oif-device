"""
OSQuery xprotect_reports ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class XprotectReports(BaseModel):
    """
    Database of XProtect matches (if user generated/sent an XProtect report).
    """
    name = TextField(help_text="Description of XProtected malware")
    user_action = TextField(help_text="Action taken by user after prompted")
    time = TextField(help_text="Quarantine alert time")

    class Meta:
        table_name = "xprotect_reports"
