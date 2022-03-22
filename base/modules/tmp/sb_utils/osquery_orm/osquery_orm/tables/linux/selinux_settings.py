"""
OSQuery selinux_settings ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class SelinuxSettings(BaseModel):
    """
    Track active SELinux settings.
    Examples:
        SELECT * FROM selinux_settings WHERE key = 'enforce'
    """
    scope = TextField(help_text="Where the key is located inside the SELinuxFS mount point.")
    key = TextField(help_text="Key or class name.")
    value = TextField(help_text="Active value.")

    class Meta:
        table_name = "selinux_settings"
