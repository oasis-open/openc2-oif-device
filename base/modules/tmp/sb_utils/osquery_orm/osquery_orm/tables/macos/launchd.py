"""
OSQuery launchd ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Launchd(BaseModel):
    """
    LaunchAgents and LaunchDaemons from default search paths.
    """
    path = TextField(help_text="Path to daemon or agent plist")  # {'index': True}
    name = TextField(help_text="File name of plist (used by launchd)")
    label = TextField(help_text="Daemon or agent service name")
    program = TextField(help_text="Path to target program")
    run_at_load = TextField(help_text="Should the program run on launch load")
    keep_alive = TextField(help_text="Should the process be restarted if killed")
    on_demand = TextField(help_text="Deprecated key, replaced by keep_alive")
    disabled = TextField(help_text="Skip loading this daemon or agent on boot")
    username = TextField(help_text="Run this daemon or agent as this username")
    groupname = TextField(help_text="Run this daemon or agent as this group")
    stdout_path = TextField(help_text="Pipe stdout to a target path")
    stderr_path = TextField(help_text="Pipe stderr to a target path")
    start_interval = TextField(help_text="Frequency to run in seconds")
    program_arguments = TextField(help_text="Command line arguments passed to program")
    watch_paths = TextField(help_text="Key that launches daemon or agent if path is modified")
    queue_directories = TextField(help_text="Similar to watch_paths but only with non-empty directories")
    inetd_compatibility = TextField(help_text="Run this daemon or agent as it was launched from inetd")
    start_on_mount = TextField(help_text="Run daemon or agent every time a filesystem is mounted")
    root_directory = TextField(help_text="Key used to specify a directory to chroot to before launch")
    working_directory = TextField(help_text="Key used to specify a directory to chdir to before launch")
    process_type = TextField(help_text="Key describes the intended purpose of the job")

    class Meta:
        table_name = "launchd"
