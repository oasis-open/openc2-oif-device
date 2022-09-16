"""
OSQuery docker_volumes ORM
"""
from ....orm import BaseModel
from peewee import TextField


class DockerVolumes(BaseModel):
    """
    Docker volumes information.
    Examples:
        select * from docker_volumes
        select * from docker_volumes where name = 'btrfs'
    """
    name = TextField(help_text="Volume name")  # {'index': True}
    driver = TextField(help_text="Volume driver")
    mount_point = TextField(help_text="Mount point")
    type = TextField(help_text="Volume type")

    class Meta:
        table_name = "docker_volumes"
