"""
OSQuery chocolatey_packages ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class ChocolateyPackages(BaseModel):
    """
    Chocolatey packages installed in a system.
    """
    name = TextField(help_text="Package display name")
    version = TextField(help_text="Package-supplied version")
    summary = TextField(help_text="Package-supplied summary")
    author = TextField(help_text="Optional package author")
    license = TextField(help_text="License under which package is launched")
    path = TextField(help_text="Path at which this package resides")

    class Meta:
        table_name = "chocolatey_packages"
