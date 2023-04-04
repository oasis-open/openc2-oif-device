"""
OSQuery suid_bin ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class SuidBin(BaseModel):
    """
    suid binaries in common locations.
    """
    path = TextField(help_text="Binary path")
    username = TextField(help_text="Binary owner username")
    groupname = TextField(help_text="Binary owner group")
    permissions = TextField(help_text="Binary permissions")

    class Meta:
        table_name = "suid_bin"


# OS specific properties for Linux
class Linux_SuidBin(SuidBin):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "suid_bin"
