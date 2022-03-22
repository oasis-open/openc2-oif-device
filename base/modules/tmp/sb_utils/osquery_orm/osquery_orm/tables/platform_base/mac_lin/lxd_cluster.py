"""
OSQuery lxd_cluster ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class LxdCluster(BaseModel):
    """
    LXD cluster information.
    Examples:
        select * from lxd_cluster
    """
    server_name = TextField(help_text="Name of the LXD server node")
    enabled = IntegerField(help_text="Whether clustering enabled (1) or not (0) on this node")
    member_config_entity = TextField(help_text="Type of configuration parameter for this node")
    member_config_name = TextField(help_text="Name of configuration parameter")
    member_config_key = TextField(help_text="Config key")
    member_config_value = TextField(help_text="Config value")
    member_config_description = TextField(help_text="Config description")

    class Meta:
        table_name = "lxd_cluster"
