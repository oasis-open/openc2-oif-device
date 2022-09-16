"""
OSQuery apparmor_events ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class ApparmorEvents(BaseModel):
    """
    Track AppArmor events.
    """
    type = TextField(help_text="Event type")
    message = TextField(help_text="Raw audit message")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}
    apparmor = TextField(help_text="Apparmor Status like ALLOWED, DENIED etc.")
    operation = TextField(help_text="Permission requested by the process")
    parent = BigIntegerField(help_text="Parent process PID")
    profile = TextField(help_text="Apparmor profile name")
    name = TextField(help_text="Process name")
    pid = BigIntegerField(help_text="Process ID")
    comm = TextField(help_text="Command-line name of the command that was used to invoke the analyzed process")
    denied_mask = TextField(help_text="Denied permissions for the process")
    capname = TextField(help_text="Capability requested by the process")
    fsuid = BigIntegerField(help_text="Filesystem user ID")
    ouid = BigIntegerField(help_text="Object owner\'s user ID")
    capability = BigIntegerField(help_text="Capability number")
    requested_mask = TextField(help_text="Requested access mask")
    info = TextField(help_text="Additional information")
    error = TextField(help_text="Error information")
    namespace = TextField(help_text="AppArmor namespace")
    label = TextField(help_text="AppArmor label")

    class Meta:
        table_name = "apparmor_events"
