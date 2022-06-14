"""
OSQuery osquery_flags ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OsqueryFlags(BaseModel):
    """
    Configurable flags that modify osquery\'s behavior.
    """
    name = TextField(help_text="Flag name")
    type = TextField(help_text="Flag type")
    description = TextField(help_text="Flag description")
    default_value = TextField(help_text="Flag default value")
    value = TextField(help_text="Flag value")
    shell_only = IntegerField(help_text="Is the flag shell only?")

    class Meta:
        table_name = "osquery_flags"
