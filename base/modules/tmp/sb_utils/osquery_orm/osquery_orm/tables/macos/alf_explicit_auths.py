"""
OSQuery alf_explicit_auths ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class AlfExplicitAuths(BaseModel):
    """
    ALF services explicitly allowed to perform networking.
    """
    process = TextField(help_text="Process name explicitly allowed")

    class Meta:
        table_name = "alf_explicit_auths"
