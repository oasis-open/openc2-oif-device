"""
OSQuery powershell_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, DoubleField, IntegerField, TextField


class PowershellEvents(BaseModel):
    """
    Powershell script blocks reconstructed to their full script content, this table requires script block logging to be enabled.
    Examples:
        select * from powershell_events;
        select * from powershell_events where script_text like '%Invoke-Mimikatz%';
        select * from powershell_events where cosine_similarity < 0.25;
    """
    time = BigIntegerField(help_text="Timestamp the event was received by the osquery event publisher")
    datetime = TextField(help_text="System time at which the Powershell script event occurred")
    script_block_id = TextField(help_text="The unique GUID of the powershell script to which this block belongs")
    script_block_count = IntegerField(help_text="The total number of script blocks for this script")
    script_text = TextField(help_text="The text content of the Powershell script")
    script_name = TextField(help_text="The name of the Powershell script")
    script_path = TextField(help_text="The path for the Powershell script")
    cosine_similarity = DoubleField(help_text="How similar the Powershell script is to a provided \'normal\' character frequency")

    class Meta:
        table_name = "powershell_events"
