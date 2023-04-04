"""
OSQuery ntfs_journal_events ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class NtfsJournalEvents(BaseModel):
    """
    Track time/action changes to files specified in configuration data.
    """
    action = TextField(help_text="Change action (Write, Delete, etc)")
    category = TextField(help_text="The category that the event originated from")
    old_path = TextField(help_text="Old path (renames only)")
    path = TextField(help_text="Path")
    record_timestamp = TextField(help_text="Journal record timestamp")
    record_usn = TextField(help_text="The update sequence number that identifies the journal record")
    node_ref_number = TextField(help_text="The ordinal that associates a journal record with a filename")
    parent_ref_number = TextField(help_text="The ordinal that associates a journal record with a filename\'s parent directory")
    drive_letter = TextField(help_text="The drive letter identifying the source journal")
    file_attributes = TextField(help_text="File attributes")
    partial = BigIntegerField(help_text="Set to 1 if either path or old_path only contains the file or folder name")
    time = BigIntegerField(help_text="Time of file event")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "ntfs_journal_events"
