"""
OSQuery etc_protocols ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class EtcProtocols(BaseModel):
    """
    Line-parsed /etc/protocols.
    """
    name = TextField(help_text="Protocol name")
    number = IntegerField(help_text="Protocol number")
    alias = TextField(help_text="Protocol alias")
    comment = TextField(help_text="Comment with protocol description")

    class Meta:
        table_name = "etc_protocols"
