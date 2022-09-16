"""
OSQuery portage_packages ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class PortagePackages(BaseModel):
    """
    List of currently installed packages.
    """
    package = TextField(help_text="Package name")
    version = TextField(help_text="The version which are affected by the use flags, empty means all")
    slot = TextField(help_text="The slot used by package")
    build_time = BigIntegerField(help_text="Unix time when package was built")
    repository = TextField(help_text="From which repository the ebuild was used")
    eapi = BigIntegerField(help_text="The eapi for the ebuild")
    size = BigIntegerField(help_text="The size of the package")
    world = IntegerField(help_text="If package is in the world file")

    class Meta:
        table_name = "portage_packages"
