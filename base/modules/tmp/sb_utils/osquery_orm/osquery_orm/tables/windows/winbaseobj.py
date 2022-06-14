"""
OSQuery winbaseobj ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Winbaseobj(BaseModel):
    """
    Lists named Windows objects in the default object directories, across all terminal services sessions.  Example Windows ojbect types include Mutexes, Events, Jobs and Semaphors.
    Examples:
        select object_name, object_type from winbaseobj
        select * from winbaseobj where type='Mutant'
    """
    session_id = IntegerField(help_text="Terminal Services Session Id")
    object_name = TextField(help_text="Object Name")
    object_type = TextField(help_text="Object Type")

    class Meta:
        table_name = "winbaseobj"
