"""
OSQuery atom_packages ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class AtomPackages(BaseModel):
    """
    Lists all atom packages in a directory or globally installed in a system.
    Examples:
        select * from atom_packages
    """
    name = TextField(help_text="Package display name")
    version = TextField(help_text="Package supplied version")
    description = TextField(help_text="Package supplied description")
    path = TextField(help_text="Package\'s package.json path")
    license = TextField(help_text="License for package")
    homepage = TextField(help_text="Package supplied homepage")
    uid = BigIntegerField(help_text="The local user that owns the plugin")  # {'index': True}

    class Meta:
        table_name = "atom_packages"
