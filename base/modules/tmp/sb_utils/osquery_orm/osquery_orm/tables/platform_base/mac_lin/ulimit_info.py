"""
OSQuery ulimit_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class UlimitInfo(BaseModel):
    """
    System resource usage limits.
    Examples:
        select * from ulimit_info
    """
    type = TextField(help_text="System resource to be limited")
    soft_limit = TextField(help_text="Current limit value")
    hard_limit = TextField(help_text="Maximum limit value")

    class Meta:
        table_name = "ulimit_info"
