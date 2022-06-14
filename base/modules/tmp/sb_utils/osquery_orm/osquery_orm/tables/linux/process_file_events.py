"""
OSQuery process_file_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class ProcessFileEvents(BaseModel):
    """
    A File Integrity Monitor implementation using the audit service.
    """
    operation = TextField(help_text="Operation type")
    pid = BigIntegerField(help_text="Process ID")
    ppid = BigIntegerField(help_text="Parent process ID")
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    executable = TextField(help_text="The executable path")
    partial = TextField(help_text="True if this is a partial event (i.e.: this process existed before we started osquery)")
    cwd = TextField(help_text="The current working directory of the process")
    path = TextField(help_text="The path associated with the event")
    dest_path = TextField(help_text="The canonical path associated with the event")
    uid = TextField(help_text="The uid of the process performing the action")
    gid = TextField(help_text="The gid of the process performing the action")
    auid = TextField(help_text="Audit user ID of the process using the file")
    euid = TextField(help_text="Effective user ID of the process using the file")
    egid = TextField(help_text="Effective group ID of the process using the file")
    fsuid = TextField(help_text="Filesystem user ID of the process using the file")
    fsgid = TextField(help_text="Filesystem group ID of the process using the file")
    suid = TextField(help_text="Saved user ID of the process using the file")
    sgid = TextField(help_text="Saved group ID of the process using the file")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "process_file_events"
