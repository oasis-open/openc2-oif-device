"""
OSQuery alf_exceptions ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class AlfExceptions(BaseModel):
    """
    OS X application layer firewall (ALF) service exceptions.
    """
    path = TextField(help_text="Path to the executable that is excepted")
    state = IntegerField(help_text="Firewall exception state")

    class Meta:
        table_name = "alf_exceptions"
