"""
OSQuery bpf_process_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class BpfProcessEvents(BaseModel):
    """
    Track time/action process executions.
    """
    tid = BigIntegerField(help_text="Thread ID")
    pid = BigIntegerField(help_text="Process ID")
    parent = BigIntegerField(help_text="Parent process ID")
    uid = BigIntegerField(help_text="User ID")
    gid = BigIntegerField(help_text="Group ID")
    cid = IntegerField(help_text="Cgroup ID")
    exit_code = TextField(help_text="Exit code of the system call")
    probe_error = IntegerField(help_text="Set to 1 if one or more buffers could not be captured")
    syscall = TextField(help_text="System call name")
    path = TextField(help_text="Binary path")
    cwd = TextField(help_text="Current working directory")
    cmdline = TextField(help_text="Command line arguments")
    duration = IntegerField(help_text="How much time was spent inside the syscall (nsecs)")
    json_cmdline = TextField(help_text="Command line arguments, in JSON format")  # {'hidden': True}
    ntime = TextField(help_text="The nsecs uptime timestamp as obtained from BPF")
    time = BigIntegerField(help_text="Time of execution in UNIX time")  # {'hidden': True}
    eid = IntegerField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "bpf_process_events"
