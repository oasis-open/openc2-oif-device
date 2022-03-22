"""
OSQuery bpf_socket_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class BpfSocketEvents(BaseModel):
    """
    Track network socket opens and closes.
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
    path = TextField(help_text="Path of executed file")
    fd = TextField(help_text="The file description for the process socket")
    family = IntegerField(help_text="The Internet protocol family ID")
    type = IntegerField(help_text="The socket type")
    protocol = IntegerField(help_text="The network protocol ID")
    local_address = TextField(help_text="Local address associated with socket")
    remote_address = TextField(help_text="Remote address associated with socket")
    local_port = IntegerField(help_text="Local network protocol port number")
    remote_port = IntegerField(help_text="Remote network protocol port number")
    duration = IntegerField(help_text="How much time was spent inside the syscall (nsecs)")
    ntime = TextField(help_text="The nsecs uptime timestamp as obtained from BPF")
    time = BigIntegerField(help_text="Time of execution in UNIX time")  # {'hidden': True}
    eid = IntegerField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "bpf_socket_events"
