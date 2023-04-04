"""
OSQuery windows_crashes ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class WindowsCrashes(BaseModel):
    """
    Extracted information from Windows crash logs (Minidumps).
    Examples:
        select * from windows_crashes
        select * from windows_crashes where module like '%electron.exe%'
        select * from windows_crashes where datetime < '2016-10-14'
        select * from windows_crashes where registers like '%rax=0000000000000004%'
        select * from windows_crashes where stack_trace like '%vlc%'
    """
    datetime = TextField(help_text="Timestamp (log format) of the crash")
    module = TextField(help_text="Path of the crashed module within the process")
    path = TextField(help_text="Path of the executable file for the crashed process")
    pid = BigIntegerField(help_text="Process ID of the crashed process")
    tid = BigIntegerField(help_text="Thread ID of the crashed thread")
    version = TextField(help_text="File version info of the crashed process")
    process_uptime = BigIntegerField(help_text="Uptime of the process in seconds")
    stack_trace = TextField(help_text="Multiple stack frames from the stack trace")
    exception_code = TextField(help_text="The Windows exception code")
    exception_message = TextField(help_text="The NTSTATUS error message associated with the exception code")
    exception_address = TextField(help_text="Address (in hex) where the exception occurred")
    registers = TextField(help_text="The values of the system registers")
    command_line = TextField(help_text="Command-line string passed to the crashed process")
    current_directory = TextField(help_text="Current working directory of the crashed process")
    username = TextField(help_text="Username of the user who ran the crashed process")
    machine_name = TextField(help_text="Name of the machine where the crash happened")
    major_version = IntegerField(help_text="Windows major version of the machine")
    minor_version = IntegerField(help_text="Windows minor version of the machine")
    build_number = IntegerField(help_text="Windows build number of the crashing machine")
    type = TextField(help_text="Type of crash log")
    crash_path = TextField(help_text="Path of the log file")

    class Meta:
        table_name = "windows_crashes"
