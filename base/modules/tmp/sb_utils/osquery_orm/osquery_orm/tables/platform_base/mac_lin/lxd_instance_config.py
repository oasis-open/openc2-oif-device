"""
OSQuery lxd_instance_config ORM
"""
from ....orm import BaseModel
from peewee import TextField


class LxdInstanceConfig(BaseModel):
    """
    LXD instance configuration information.
    Examples:
        select * from lxd_instance_config where name = 'hello'
    """
    name = TextField(help_text="Instance name")  # {'index': True, 'required': True}
    key = TextField(help_text="Configuration parameter name")
    value = TextField(help_text="Configuration parameter value")

    class Meta:
        table_name = "lxd_instance_config"
