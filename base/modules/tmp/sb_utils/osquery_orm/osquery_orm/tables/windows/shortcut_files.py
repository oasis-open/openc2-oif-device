"""
OSQuery shortcut_files ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class ShortcutFiles(BaseModel):
    """
    View data about Windows Shortcut files.
    Examples:
        select * from shortcut_files;
    """
    path = TextField(help_text="Directory name.")  # {'required': True}
    target_path = TextField(help_text="Target file path")
    target_modified = IntegerField(help_text="Target Modified time.")
    target_created = IntegerField(help_text="Target Created time.")
    target_accessed = IntegerField(help_text="Target Accessed time.")
    target_size = BigIntegerField(help_text="Size of target file.")
    relative_path = TextField(help_text="Relative path to target file from lnk file.")
    local_path = TextField(help_text="Local system path to target file.")
    working_path = TextField(help_text="Target file directory.")
    icon_path = TextField(help_text="Lnk file icon location.")
    common_path = TextField(help_text="Common system path to target file.")
    command_args = TextField(help_text="Command args passed to lnk file.")
    hostname = TextField(help_text="Optional hostname of the target file.")
    share_name = TextField(help_text="Share name of the target file.")
    device_type = TextField(help_text="Device containing the target file.")
    volume_serial = TextField(help_text="Volume serial number.")
    mft_entry = BigIntegerField(help_text="Target mft entry.")
    mft_sequence = IntegerField(help_text="Target mft sequence.")
    description = TextField(help_text="Lnk file description.")

    class Meta:
        table_name = "shortcut_files"
