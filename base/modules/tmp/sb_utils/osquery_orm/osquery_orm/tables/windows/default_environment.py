"""
OSQuery default_environment ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class DefaultEnvironment(BaseModel):
    """
    Default environment variables and values.
    """
    variable = TextField(help_text="Name of the environment variable")
    value = TextField(help_text="Value of the environment variable")
    expand = IntegerField(help_text="1 if the variable needs expanding, 0 otherwise")

    class Meta:
        table_name = "default_environment"
