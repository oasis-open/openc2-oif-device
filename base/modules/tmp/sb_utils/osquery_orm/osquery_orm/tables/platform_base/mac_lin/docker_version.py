"""
OSQuery docker_version ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class DockerVersion(BaseModel):
    """
    Docker version information.
    Examples:
        select version from docker_version
    """
    version = TextField(help_text="Docker version")
    api_version = TextField(help_text="API version")
    min_api_version = TextField(help_text="Minimum API version supported")
    git_commit = TextField(help_text="Docker build git commit")
    go_version = TextField(help_text="Go version")
    os = TextField(help_text="Operating system")
    arch = TextField(help_text="Hardware architecture")
    kernel_version = TextField(help_text="Kernel version")
    build_time = TextField(help_text="Build time")

    class Meta:
        table_name = "docker_version"
