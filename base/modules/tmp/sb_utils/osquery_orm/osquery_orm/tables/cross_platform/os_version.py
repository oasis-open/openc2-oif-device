"""
OSQuery os_version ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class OSVersion(BaseModel):
    """
    A single row containing the operating system name and version.
    """
    name = TextField(help_text="Distribution or product name")
    version = TextField(help_text="Pretty, suitable for presentation, OS version")
    major = IntegerField(help_text="Major release version")
    minor = IntegerField(help_text="Minor release version")
    patch = IntegerField(help_text="Optional patch release")
    build = TextField(help_text="Optional build-specific or variant string")
    platform = TextField(help_text="OS Platform or ID")
    platform_like = TextField(help_text="Closely related platforms")
    codename = TextField(help_text="OS version codename")
    arch = TextField(help_text="OS Architecture")

    class Meta:
        table_name = "os_version"


# OS specific properties for Windows
class Windows_OSVersion(OSVersion):
    install_date = BigIntegerField(help_text="The install date of the OS.")

    class Meta:
        table_name = "os_version"


# OS specific properties for Linux
class Linux_OSVersion(OSVersion):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "os_version"
