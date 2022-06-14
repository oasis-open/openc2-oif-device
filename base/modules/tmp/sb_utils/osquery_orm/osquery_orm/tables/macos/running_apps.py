"""
OSQuery running_apps ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class RunningApps(BaseModel):
    """
    macOS applications currently running on the host system.
    """
    pid = IntegerField(help_text="The pid of the application")  # {'index': True}
    bundle_identifier = TextField(help_text="The bundle identifier of the application")
    is_active = IntegerField(help_text="1 if the application is in focus, 0 otherwise")  # {'additional': True}

    class Meta:
        table_name = "running_apps"
