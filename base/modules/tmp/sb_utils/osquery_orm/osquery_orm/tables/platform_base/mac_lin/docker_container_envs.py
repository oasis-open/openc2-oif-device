"""
OSQuery docker_container_envs ORM
"""
from ....orm import BaseModel
from peewee import TextField


class DockerContainerEnvs(BaseModel):
    """
    Docker container environment variables.
    Examples:
        select * from docker_container_envs
        select * from docker_container_envs where id = '1234567890abcdef'
        select * from docker_container_envs where id = '11b2399e1426d906e62a0c657650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'index': True}
    key = TextField(help_text="Environment variable name")
    value = TextField(help_text="Environment variable value")

    class Meta:
        table_name = "docker_container_envs"
