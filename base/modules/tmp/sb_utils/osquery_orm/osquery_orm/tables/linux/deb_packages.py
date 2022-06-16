"""
OSQuery deb_packages ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DebPackages(BaseModel):
    """
    The installed DEB package database.
    """
    name = TextField(help_text="Package name")
    version = TextField(help_text="Package version")
    source = TextField(help_text="Package source")
    size = BigIntegerField(help_text="Package size in bytes")
    arch = TextField(help_text="Package architecture")
    revision = TextField(help_text="Package revision")
    status = TextField(help_text="Package status")
    maintainer = TextField(help_text="Package maintainer")
    section = TextField(help_text="Package section")
    priority = TextField(help_text="Package priority")

    class Meta:
        table_name = "deb_packages"


# OS specific properties for Linux
class Linux_DebPackages(DebPackages):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "deb_packages"
