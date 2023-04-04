"""
OSQuery docker_container_mounts ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class DockerContainerMounts(BaseModel):
    """
    Docker container mounts.
    Examples:
        select * from docker_container_mounts
        select * from docker_container_mounts where id = '1234567890abcdef'
        select * from docker_container_mounts where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'index': True}
    type = TextField(help_text="Type of mount (bind, volume)")
    name = TextField(help_text="Optional mount name")  # {'index': True}
    source = TextField(help_text="Source path on host")
    destination = TextField(help_text="Destination path inside container")
    driver = TextField(help_text="Driver providing the mount")
    mode = TextField(help_text="Mount options (rw, ro)")
    rw = IntegerField(help_text="1 if read/write. 0 otherwise")
    propagation = TextField(help_text="Mount propagation")

    class Meta:
        table_name = "docker_container_mounts"
