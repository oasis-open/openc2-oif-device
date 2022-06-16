"""
OSQuery yara_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class YaraEvents(BaseModel):
    """
    Track YARA matches for files specified in configuration data.
    """
    target_path = TextField(help_text="The path scanned")
    category = TextField(help_text="The category of the file")
    action = TextField(help_text="Change action (UPDATE, REMOVE, etc)")
    transaction_id = BigIntegerField(help_text="ID used during bulk update")
    matches = TextField(help_text="List of YARA matches")
    count = IntegerField(help_text="Number of YARA matches")
    strings = TextField(help_text="Matching strings")
    tags = TextField(help_text="Matching tags")
    time = BigIntegerField(help_text="Time of the scan")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "yara_events"
