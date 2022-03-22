"""
OSQuery osquery_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OsqueryInfo(BaseModel):
    """
    Top level information about the running version of osquery.
    """
    pid = IntegerField(help_text="Process (or thread/handle) ID")
    uuid = TextField(help_text="Unique ID provided by the system")
    instance_id = TextField(help_text="Unique, long-lived ID per instance of osquery")
    version = TextField(help_text="osquery toolkit version")
    config_hash = TextField(help_text="Hash of the working configuration state")
    config_valid = IntegerField(help_text="1 if the config was loaded and considered valid, else 0")
    extensions = TextField(help_text="osquery extensions status")
    build_platform = TextField(help_text="osquery toolkit build platform")
    build_distro = TextField(help_text="osquery toolkit platform distribution name (os version)")
    start_time = IntegerField(help_text="UNIX time in seconds when the process started")
    watcher = IntegerField(help_text="Process (or thread/handle) ID of optional watcher process")
    platform_mask = IntegerField(help_text="The osquery platform bitmask")

    class Meta:
        table_name = "osquery_info"
