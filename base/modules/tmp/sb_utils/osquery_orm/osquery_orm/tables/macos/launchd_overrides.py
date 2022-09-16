"""
OSQuery launchd_overrides ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class LaunchdOverrides(BaseModel):
    """
    Override keys, per user, for LaunchDaemons and Agents.
    """
    label = TextField(help_text="Daemon or agent service name")
    key = TextField(help_text="Name of the override key")
    value = TextField(help_text="Overridden value")
    uid = BigIntegerField(help_text="User ID applied to the override, 0 applies to all")
    path = TextField(help_text="Path to daemon or agent plist")

    class Meta:
        table_name = "launchd_overrides"
