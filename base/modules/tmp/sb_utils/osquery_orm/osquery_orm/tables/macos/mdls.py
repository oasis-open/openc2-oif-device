"""
OSQuery mdls ORM
"""
from ...orm import BaseModel
from peewee import TextField


class Mdls(BaseModel):
    """
    Query file metadata in the Spotlight database.
    Examples:
        select * from mdls where path = '/Users/testuser/Desktop/testfile';
    """
    path = TextField(help_text="Path of the file")  # {'required': True}
    key = TextField(help_text="Name of the metadata key")
    value = TextField(help_text="Value stored in the metadata key")
    valuetype = TextField(help_text="CoreFoundation type of data stored in value")  # {'hidden': True}

    class Meta:
        table_name = "mdls"
