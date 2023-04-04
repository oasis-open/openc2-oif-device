"""
OSQuery users ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Users(BaseModel):
    """
    Local user accounts (including domain accounts that have logged on locally (Windows)).
    Examples:
        select * from users where uid = 1000
        select * from users where username = 'root'
        select count(*) from users u, user_groups ug where u.uid = ug.uid
    """
    uid = BigIntegerField(help_text="User ID")  # {'index': True}
    gid = BigIntegerField(help_text="Group ID (unsigned)")
    uid_signed = BigIntegerField(help_text="User ID as int64 signed (Apple)")
    gid_signed = BigIntegerField(help_text="Default group ID as int64 signed (Apple)")
    username = TextField(help_text="Username")  # {'additional': True}
    description = TextField(help_text="Optional user description")
    directory = TextField(help_text="User\'s home directory")
    shell = TextField(help_text="User\'s configured default shell")
    uuid = TextField(help_text="User\'s UUID (Apple) or SID (Windows)")  # {'index': True}

    class Meta:
        table_name = "users"


# OS specific properties for Windows
class Windows_Users(Users):
    type = TextField(help_text="Whether the account is roaming (domain), local, or a system profile")

    class Meta:
        table_name = "users"


# OS specific properties for MacOS
class MacOS_Users(Users):
    is_hidden = IntegerField(help_text="IsHidden attribute set in OpenDirectory")

    class Meta:
        table_name = "users"


# OS specific properties for Linux
class Linux_Users(Users):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "users"
