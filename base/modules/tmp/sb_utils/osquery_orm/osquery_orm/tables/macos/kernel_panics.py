"""
OSQuery kernel_panics ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class KernelPanics(BaseModel):
    """
    System kernel panic logs.
    """
    path = TextField(help_text="Location of log file")
    time = TextField(help_text="Formatted time of the event")
    registers = TextField(help_text="A space delimited line of register:value pairs")
    frame_backtrace = TextField(help_text="Backtrace of the crashed module")
    module_backtrace = TextField(help_text="Modules appearing in the crashed module\'s backtrace")
    dependencies = TextField(help_text="Module dependencies existing in crashed module\'s backtrace")
    name = TextField(help_text="Process name corresponding to crashed thread")
    os_version = TextField(help_text="Version of the operating system")
    kernel_version = TextField(help_text="Version of the system kernel")
    system_model = TextField(help_text="Physical system model, for example \'MacBookPro12,1 (Mac-E43C1C25D4880AD6)\'")
    uptime = BigIntegerField(help_text="System uptime at kernel panic in nanoseconds")
    last_loaded = TextField(help_text="Last loaded module before panic")
    last_unloaded = TextField(help_text="Last unloaded module before panic")

    class Meta:
        table_name = "kernel_panics"
