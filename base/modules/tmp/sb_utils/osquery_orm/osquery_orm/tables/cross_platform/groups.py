"""
OSQuery groups ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Groups(BaseModel):
    """
    Local system groups.
    Examples:
        select * from groups where gid = 0
    """
    gid = BigIntegerField(help_text="Unsigned int64 group ID")  # {'index': True}
    gid_signed = BigIntegerField(help_text="A signed int64 version of gid")
    groupname = TextField(help_text="Canonical local group name")

    class Meta:
        table_name = "groups"


# OS specific properties for Windows
class Windows_Groups(Groups):
    group_sid = TextField(help_text="Unique group ID")  # {'index': True}
    comment = TextField(help_text="Remarks or comments associated with the group")

    class Meta:
        table_name = "groups"


# OS specific properties for MacOS
class MacOS_Groups(Groups):
    is_hidden = IntegerField(help_text="IsHidden attribute set in OpenDirectory")

    class Meta:
        table_name = "groups"


# OS specific properties for Linux
class Linux_Groups(Groups):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "groups"
