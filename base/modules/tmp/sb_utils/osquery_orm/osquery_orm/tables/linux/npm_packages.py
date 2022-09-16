"""
OSQuery npm_packages ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class NpmPackages(BaseModel):
    """
    Lists all npm packages in a directory or globally installed in a system.
    Examples:
        select * from npm_packages
        select * from npm_packages where directory = '/home/user/my_project'
    """
    name = TextField(help_text="Package display name")
    version = TextField(help_text="Package supplied version")
    description = TextField(help_text="Package supplied description")
    author = TextField(help_text="Package author name")
    license = TextField(help_text="License for package")
    path = TextField(help_text="Module\'s package.json path")
    directory = TextField(help_text="Node module\'s directory where this package is located")  # {'index': True}

    class Meta:
        table_name = "npm_packages"


# OS specific properties for Linux
class Linux_NpmPackages(NpmPackages):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "npm_packages"
