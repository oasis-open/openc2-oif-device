"""
OSQuery system_controls ORM
"""
from ....orm import BaseModel
from peewee import TextField


class SystemControls(BaseModel):
    """
    sysctl names, values, and settings information.
    """
    name = TextField(help_text="Full sysctl MIB name")  # {'index': True}
    oid = TextField(help_text="Control MIB")  # {'additional': True}
    subsystem = TextField(help_text="Subsystem ID, control type")  # {'additional': True}
    current_value = TextField(help_text="Value of setting")
    config_value = TextField(help_text="The MIB value set in /etc/sysctl.conf")
    type = TextField(help_text="Data type")

    class Meta:
        table_name = "system_controls"


# OS specific properties for MacOS
class MacOS_SystemControls(SystemControls):
    field_name = TextField(help_text="Specific attribute of opaque type")

    class Meta:
        table_name = "system_controls"
