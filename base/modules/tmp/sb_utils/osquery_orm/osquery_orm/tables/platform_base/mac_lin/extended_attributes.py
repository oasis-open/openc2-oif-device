"""
OSQuery extended_attributes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class ExtendedAttributes(BaseModel):
    """
    Returns the extended attributes for files (similar to Windows ADS).
    """
    path = TextField(help_text="Absolute file path")  # {'required': True}
    directory = TextField(help_text="Directory of file(s)")  # {'required': True}
    key = TextField(help_text="Name of the value generated from the extended attribute")
    value = TextField(help_text="The parsed information from the attribute")
    base64 = IntegerField(help_text="1 if the value is base64 encoded else 0")

    class Meta:
        table_name = "extended_attributes"
