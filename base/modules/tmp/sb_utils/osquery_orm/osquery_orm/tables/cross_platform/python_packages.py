"""
OSQuery python_packages ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class PythonPackages(BaseModel):
    """
    Python packages installed in a system.
    Examples:
        select * from python_packages where directory='/usr/'
    """
    name = TextField(help_text="Package display name")
    version = TextField(help_text="Package-supplied version")
    summary = TextField(help_text="Package-supplied summary")
    author = TextField(help_text="Optional package author")
    license = TextField(help_text="License under which package is launched")
    path = TextField(help_text="Path at which this module resides")
    directory = TextField(help_text="Directory where Python modules are located")  # {'index': True}

    class Meta:
        table_name = "python_packages"


# OS specific properties for Linux
class Linux_PythonPackages(PythonPackages):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "python_packages"
