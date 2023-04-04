"""
OSQuery process_events ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class ProcessEvents(BaseModel):
    """
    Track time/action process executions.
    """
    pid = BigIntegerField(help_text="Process (or thread) ID")
    path = TextField(help_text="Path of executed file")
    mode = TextField(help_text="File mode permissions")
    cmdline = TextField(help_text="Command line arguments (argv)")
    cmdline_size = BigIntegerField(help_text="Actual size (bytes) of command line arguments")  # {'hidden': True}
    env = TextField(help_text="Environment variables delimited by spaces")  # {'aliases': ['environment'], 'hidden': True}
    env_count = BigIntegerField(help_text="Number of environment variables")  # {'aliases': ['environment_count'], 'hidden': True}
    env_size = BigIntegerField(help_text="Actual size (bytes) of environment list")  # {'aliases': ['environment_size'], 'hidden': True}
    cwd = TextField(help_text="The process current working directory")
    auid = BigIntegerField(help_text="Audit User ID at process start")
    uid = BigIntegerField(help_text="User ID at process start")
    euid = BigIntegerField(help_text="Effective user ID at process start")
    gid = BigIntegerField(help_text="Group ID at process start")
    egid = BigIntegerField(help_text="Effective group ID at process start")
    owner_uid = BigIntegerField(help_text="File owner user ID")
    owner_gid = BigIntegerField(help_text="File owner group ID")
    atime = BigIntegerField(help_text="File last access in UNIX time")  # {'aliases': ['access_time']}
    mtime = BigIntegerField(help_text="File modification in UNIX time")  # {'aliases': ['modify_time']}
    ctime = BigIntegerField(help_text="File last metadata change in UNIX time")  # {'aliases': ['change_time']}
    btime = BigIntegerField(help_text="File creation in UNIX time")  # {'aliases': ['create_time']}
    overflows = TextField(help_text="List of structures that overflowed")  # {'hidden': True}
    parent = BigIntegerField(help_text="Process parent\'s PID, or -1 if cannot be determined.")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "process_events"


# OS specific properties for MacOS
class MacOS_ProcessEvents(ProcessEvents):
    status = BigIntegerField(help_text="OpenBSM Attribute: Status of the process")

    class Meta:
        table_name = "process_events"


# OS specific properties for Linux
class Linux_ProcessEvents(ProcessEvents):
    fsuid = BigIntegerField(help_text="Filesystem user ID at process start")
    suid = BigIntegerField(help_text="Saved user ID at process start")
    fsgid = BigIntegerField(help_text="Filesystem group ID at process start")
    sgid = BigIntegerField(help_text="Saved group ID at process start")
    syscall = TextField(help_text="Syscall name: fork, vfork, clone, execve, execveat")

    class Meta:
        table_name = "process_events"
