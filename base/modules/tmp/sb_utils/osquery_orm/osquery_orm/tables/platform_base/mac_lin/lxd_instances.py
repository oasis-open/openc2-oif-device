"""
OSQuery lxd_instances ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class LxdInstances(BaseModel):
    """
    LXD instances information.
    Examples:
        select * from lxd_instances
        select * from lxd_instances where name = 'hello'
    """
    name = TextField(help_text="Instance name")  # {'index': True}
    status = TextField(help_text="Instance state (running, stopped, etc.)")
    stateful = IntegerField(help_text="Whether the instance is stateful(1) or not(0)")
    ephemeral = IntegerField(help_text="Whether the instance is ephemeral(1) or not(0)")
    created_at = TextField(help_text="ISO time of creation")
    base_image = TextField(help_text="ID of image used to launch this instance")
    architecture = TextField(help_text="Instance architecture")
    os = TextField(help_text="The OS of this instance")
    description = TextField(help_text="Instance description")
    pid = IntegerField(help_text="Instance\'s process ID")
    processes = IntegerField(help_text="Number of processes running inside this instance")

    class Meta:
        table_name = "lxd_instances"
