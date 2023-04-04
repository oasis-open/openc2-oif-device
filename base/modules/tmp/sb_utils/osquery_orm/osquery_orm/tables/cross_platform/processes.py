"""
OSQuery processes ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Processes(BaseModel):
    """
    All running processes on the host system.
    Examples:
        select * from processes where pid = 1
    """
    pid = BigIntegerField(help_text="Process (or thread) ID")  # {'index': True}
    name = TextField(help_text="The process path or shorthand argv[0]")
    path = TextField(help_text="Path to executed binary")
    cmdline = TextField(help_text="Complete argv")
    state = TextField(help_text="Process state")
    cwd = TextField(help_text="Process current working directory")
    root = TextField(help_text="Process virtual root directory")
    uid = BigIntegerField(help_text="Unsigned user ID")
    gid = BigIntegerField(help_text="Unsigned group ID")
    euid = BigIntegerField(help_text="Unsigned effective user ID")
    egid = BigIntegerField(help_text="Unsigned effective group ID")
    suid = BigIntegerField(help_text="Unsigned saved user ID")
    sgid = BigIntegerField(help_text="Unsigned saved group ID")
    on_disk = IntegerField(help_text="The process path exists yes=1, no=0, unknown=-1")
    wired_size = BigIntegerField(help_text="Bytes of unpageable memory used by process")
    resident_size = BigIntegerField(help_text="Bytes of private memory used by process")
    total_size = BigIntegerField(help_text="Total virtual memory size")  # {'aliases': ['phys_footprint']}
    user_time = BigIntegerField(help_text="CPU time in milliseconds spent in user space")
    system_time = BigIntegerField(help_text="CPU time in milliseconds spent in kernel space")
    disk_bytes_read = BigIntegerField(help_text="Bytes read from disk")
    disk_bytes_written = BigIntegerField(help_text="Bytes written to disk")
    start_time = BigIntegerField(help_text="Process start time in seconds since Epoch, in case of error -1")
    parent = BigIntegerField(help_text="Process parent\'s PID")
    pgroup = BigIntegerField(help_text="Process group")
    threads = IntegerField(help_text="Number of threads used by process")
    nice = IntegerField(help_text="Process nice level (-20 to 20, default 0)")

    class Meta:
        table_name = "processes"


# OS specific properties for Windows
class Windows_Processes(Processes):
    elevated_token = IntegerField(help_text="Process uses elevated token yes=1, no=0")
    secure_process = IntegerField(help_text="Process is secure (IUM) yes=1, no=0")
    protection_type = TextField(help_text="The protection type of the process")
    virtual_process = IntegerField(help_text="Process is virtual (e.g. System, Registry, vmmem) yes=1, no=0")
    elapsed_time = BigIntegerField(help_text="Elapsed time in seconds this process has been running.")
    handle_count = BigIntegerField(help_text="Total number of handles that the process has open. This number is the sum of the handles currently opened by each thread in the process.")
    percent_processor_time = BigIntegerField(help_text="Returns elapsed time that all of the threads of this process used the processor to execute instructions in 100 nanoseconds ticks.")

    class Meta:
        table_name = "processes"


# OS specific properties for MacOS
class MacOS_Processes(Processes):
    upid = BigIntegerField(help_text="A 64bit pid that is never reused. Returns -1 if we couldn\'t gather them from the system.")
    uppid = BigIntegerField(help_text="The 64bit parent pid that is never reused. Returns -1 if we couldn\'t gather them from the system.")
    cpu_type = IntegerField(help_text="Indicates the specific processor designed for installation.")
    cpu_subtype = IntegerField(help_text="Indicates the specific processor on which an entry may be used.")

    class Meta:
        table_name = "processes"
