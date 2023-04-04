"""
OSQuery es_process_events ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class EsProcessEvents(BaseModel):
    """
    Process execution events from EndpointSecurity.
    """
    version = IntegerField(help_text="Version of EndpointSecurity event")
    seq_num = BigIntegerField(help_text="Per event sequence number")
    global_seq_num = BigIntegerField(help_text="Global sequence number")
    pid = BigIntegerField(help_text="Process (or thread) ID")
    path = TextField(help_text="Path of executed file")
    parent = BigIntegerField(help_text="Parent process ID")
    original_parent = BigIntegerField(help_text="Original parent process ID in case of reparenting")
    cmdline = TextField(help_text="Command line arguments (argv)")
    cmdline_count = BigIntegerField(help_text="Number of command line arguments")
    env = TextField(help_text="Environment variables delimited by spaces")
    env_count = BigIntegerField(help_text="Number of environment variables")
    cwd = TextField(help_text="The process current working directory")
    uid = BigIntegerField(help_text="User ID of the process")
    euid = BigIntegerField(help_text="Effective User ID of the process")
    gid = BigIntegerField(help_text="Group ID of the process")
    egid = BigIntegerField(help_text="Effective Group ID of the process")
    username = TextField(help_text="Username")
    signing_id = TextField(help_text="Signature identifier of the process")
    team_id = TextField(help_text="Team identifier of thd process")
    cdhash = TextField(help_text="Codesigning hash of the process")
    platform_binary = IntegerField(help_text="Indicates if the binary is Apple signed binary (1) or not (0)")
    exit_code = IntegerField(help_text="Exit code of a process in case of an exit event")
    child_pid = BigIntegerField(help_text="Process ID of a child process in case of a fork event")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    event_type = TextField(help_text="Type of EndpointSecurity event")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "es_process_events"
