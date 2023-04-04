"""
OSQuery rpm_package_files ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class RpmPackageFiles(BaseModel):
    """
    RPM packages that are currently installed on the host system.
    """
    package = TextField(help_text="RPM package name")  # {'index': True}
    path = TextField(help_text="File path within the package")  # {'index': True}
    username = TextField(help_text="File default username from info DB")
    groupname = TextField(help_text="File default groupname from info DB")
    mode = TextField(help_text="File permissions mode from info DB")
    size = BigIntegerField(help_text="Expected file size in bytes from RPM info DB")
    sha256 = TextField(help_text="SHA256 file digest from RPM info DB")

    class Meta:
        table_name = "rpm_package_files"
