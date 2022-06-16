"""
OSQuery docker_container_processes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, DoubleField, IntegerField, TextField


class DockerContainerProcesses(BaseModel):
    """
    Docker container processes.
    Examples:
        select * from docker_container_processes where id = '1234567890abcdef'
        select * from docker_container_processes where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'index': True, 'required': True}
    pid = BigIntegerField(help_text="Process ID")  # {'index': True}
    name = TextField(help_text="The process path or shorthand argv[0]")
    cmdline = TextField(help_text="Complete argv")
    state = TextField(help_text="Process state")
    uid = BigIntegerField(help_text="User ID")
    gid = BigIntegerField(help_text="Group ID")
    euid = BigIntegerField(help_text="Effective user ID")
    egid = BigIntegerField(help_text="Effective group ID")
    suid = BigIntegerField(help_text="Saved user ID")
    sgid = BigIntegerField(help_text="Saved group ID")
    wired_size = BigIntegerField(help_text="Bytes of unpageable memory used by process")
    resident_size = BigIntegerField(help_text="Bytes of private memory used by process")
    total_size = BigIntegerField(help_text="Total virtual memory size")  # {'aliases': ['phys_footprint']}
    start_time = BigIntegerField(help_text="Process start in seconds since boot (non-sleeping)")
    parent = BigIntegerField(help_text="Process parent\'s PID")
    pgroup = BigIntegerField(help_text="Process group")
    threads = IntegerField(help_text="Number of threads used by process")
    nice = IntegerField(help_text="Process nice level (-20 to 20, default 0)")
    user = TextField(help_text="User name")
    time = TextField(help_text="Cumulative CPU time. [DD-]HH:MM:SS format")
    cpu = DoubleField(help_text="CPU utilization as percentage")
    mem = DoubleField(help_text="Memory utilization as percentage")

    class Meta:
        table_name = "docker_container_processes"
