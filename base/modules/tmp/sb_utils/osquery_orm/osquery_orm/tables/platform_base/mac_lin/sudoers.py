"""
OSQuery sudoers ORM
"""
from ....orm import BaseModel
from peewee import TextField


class Sudoers(BaseModel):
    """
    Rules for running commands as other users via sudo.
    """
    source = TextField(help_text="Source file containing the given rule")
    header = TextField(help_text="Symbol for given rule")
    rule_details = TextField(help_text="Rule definition")

    class Meta:
        table_name = "sudoers"
