"""
OSQuery shellbags ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Shellbags(BaseModel):
    """
    Shows directories accessed via Windows Explorer.
    Examples:
        select * from shellbags;
    """
    sid = TextField(help_text="User SID")
    source = TextField(help_text="Shellbags source Registry file")
    path = TextField(help_text="Directory name.")
    modified_time = BigIntegerField(help_text="Directory Modified time.")
    created_time = BigIntegerField(help_text="Directory Created time.")
    accessed_time = BigIntegerField(help_text="Directory Accessed time.")
    mft_entry = BigIntegerField(help_text="Directory master file table entry.")
    mft_sequence = IntegerField(help_text="Directory master file table sequence.")

    class Meta:
        table_name = "shellbags"
