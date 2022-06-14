"""
OSQuery docker_container_fs_changes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class DockerContainerFsChanges(BaseModel):
    """
    Changes to files or directories on container\'s filesystem.
    Examples:
        select * from docker_container_fs_changes where id = '1234567890abcdef'
        select * from docker_container_fs_changes where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'index': True, 'required': True}
    path = TextField(help_text="FIle or directory path relative to rootfs")
    change_type = TextField(help_text="Type of change: C:Modified, A:Added, D:Deleted")

    class Meta:
        table_name = "docker_container_fs_changes"
