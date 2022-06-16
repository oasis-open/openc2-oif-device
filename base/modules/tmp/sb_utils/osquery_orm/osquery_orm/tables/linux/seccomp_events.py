"""
OSQuery seccomp_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class SeccompEvents(BaseModel):
    """
    A virtual table that tracks seccomp events.
    """
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    auid = BigIntegerField(help_text="Audit user ID (loginuid) of the user who started the analyzed process")
    uid = BigIntegerField(help_text="User ID of the user who started the analyzed process")
    gid = BigIntegerField(help_text="Group ID of the user who started the analyzed process")
    ses = BigIntegerField(help_text="Session ID of the session from which the analyzed process was invoked")
    pid = BigIntegerField(help_text="Process ID")
    comm = TextField(help_text="Command-line name of the command that was used to invoke the analyzed process")
    exe = TextField(help_text="The path to the executable that was used to invoke the analyzed process")
    sig = BigIntegerField(help_text="Signal value sent to process by seccomp")
    arch = TextField(help_text="Information about the CPU architecture")
    syscall = TextField(help_text="Type of the system call")
    compat = BigIntegerField(help_text="Is system call in compatibility mode")
    ip = TextField(help_text="Instruction pointer value")
    code = TextField(help_text="The seccomp action")

    class Meta:
        table_name = "seccomp_events"
