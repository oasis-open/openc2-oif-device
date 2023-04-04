"""
OSQuery homebrew_packages ORM
"""
from ...orm import BaseModel
from peewee import TextField


class HomebrewPackages(BaseModel):
    """
    The installed homebrew package database.
    """
    name = TextField(help_text="Package name")
    path = TextField(help_text="Package install path")
    version = TextField(help_text="Current \'linked\' version")
    prefix = TextField(help_text="Homebrew install prefix")  # {'hidden': True, 'additional': True}

    class Meta:
        table_name = "homebrew_packages"
