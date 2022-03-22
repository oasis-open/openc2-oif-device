"""
OSQuery time_machine_destinations ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class TimeMachineDestinations(BaseModel):
    """
    Locations backed up to using Time Machine.
    Examples:
        select alias, backup_date, td.destination_id, root_volume_uuid, encryption from time_machine_backups tb join time_machine_destinations td on (td.destination_id=tb.destination_id);
    """
    alias = TextField(help_text="Human readable name of drive")
    destination_id = TextField(help_text="Time Machine destination ID")
    consistency_scan_date = IntegerField(help_text="Consistency scan date")
    root_volume_uuid = TextField(help_text="Root UUID of backup volume")
    bytes_available = IntegerField(help_text="Bytes available on volume")
    bytes_used = IntegerField(help_text="Bytes used on volume")
    encryption = TextField(help_text="Last known encrypted state")

    class Meta:
        table_name = "time_machine_destinations"
