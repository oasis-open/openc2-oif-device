"""
OSQuery pkg_packages ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class PkgPackages(BaseModel):
    """
    pkgng packages that are currently installed on the host system.
    """
    name = TextField(help_text="Package name")
    version = TextField(help_text="Package version")
    flatsize = BigIntegerField(help_text="Package size in bytes")
    arch = TextField(help_text="Architecture(s) supported")

    class Meta:
        table_name = "pkg_packages"
