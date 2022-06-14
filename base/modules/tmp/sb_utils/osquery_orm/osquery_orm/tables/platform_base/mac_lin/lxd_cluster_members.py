"""
OSQuery lxd_cluster_members ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class LxdClusterMembers(BaseModel):
    """
    LXD cluster members information.
    Examples:
        select * from lxd_cluster_members
    """
    server_name = TextField(help_text="Name of the LXD server node")
    url = TextField(help_text="URL of the node")
    database = IntegerField(help_text="Whether the server is a database node (1) or not (0)")
    status = TextField(help_text="Status of the node (Online/Offline)")
    message = TextField(help_text="Message from the node (Online/Offline)")

    class Meta:
        table_name = "lxd_cluster_members"
