"""
OSQuery augeas ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Augeas(BaseModel):
    """
    Configuration files parsed by augeas.
    Examples:
        select * from augeas where path = '/etc/hosts'
    """
    node = TextField(help_text="The node path of the configuration item")  # {'index': True}
    value = TextField(help_text="The value of the configuration item")
    label = TextField(help_text="The label of the configuration item")
    path = TextField(help_text="The path to the configuration file")  # {'additional': True}

    class Meta:
        table_name = "augeas"
