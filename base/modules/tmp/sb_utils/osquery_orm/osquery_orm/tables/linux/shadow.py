"""
OSQuery shadow ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class Shadow(BaseModel):
    """
    Local system users encrypted passwords and related information. Please note, that you usually need superuser rights to access `/etc/shadow`.
    Examples:
        select * from shadow where username = 'root'
    """
    password_status = TextField(help_text="Password status")
    hash_alg = TextField(help_text="Password hashing algorithm")
    last_change = BigIntegerField(help_text="Date of last password change (starting from UNIX epoch date)")
    min = BigIntegerField(help_text="Minimal number of days between password changes")
    max = BigIntegerField(help_text="Maximum number of days between password changes")
    warning = BigIntegerField(help_text="Number of days before password expires to warn user about it")
    inactive = BigIntegerField(help_text="Number of days after password expires until account is blocked")
    expire = BigIntegerField(help_text="Number of days since UNIX epoch date until account is disabled")
    flag = BigIntegerField(help_text="Reserved")
    username = TextField(help_text="Username")  # {'index': True}

    class Meta:
        table_name = "shadow"
