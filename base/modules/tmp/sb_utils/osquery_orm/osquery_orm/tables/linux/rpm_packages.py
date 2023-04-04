"""
OSQuery rpm_packages ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class RpmPackages(BaseModel):
    """
    RPM packages that are currently installed on the host system.
    """
    name = TextField(help_text="RPM package name")  # {'index': True}
    version = TextField(help_text="Package version")  # {'index': True}
    release = TextField(help_text="Package release")  # {'index': True}
    source = TextField(help_text="Source RPM package name (optional)")
    size = BigIntegerField(help_text="Package size in bytes")
    sha1 = TextField(help_text="SHA1 hash of the package contents")
    arch = TextField(help_text="Architecture(s) supported")  # {'index': True}
    epoch = IntegerField(help_text="Package epoch value")  # {'index': True}
    install_time = IntegerField(help_text="When the package was installed")
    vendor = TextField(help_text="Package vendor")
    package_group = TextField(help_text="Package group")

    class Meta:
        table_name = "rpm_packages"


# OS specific properties for Linux
class Linux_RpmPackages(RpmPackages):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "rpm_packages"
