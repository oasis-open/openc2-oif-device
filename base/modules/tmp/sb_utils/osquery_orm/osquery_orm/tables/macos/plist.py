"""
OSQuery plist ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Plist(BaseModel):
    """
    Read and parse a plist file.
    Examples:
        select * from plist where path = '/Library/Preferences/loginwindow.plist'
    """
    key = TextField(help_text="Preference top-level key")
    subkey = TextField(help_text="Intermediate key path, includes lists/dicts")
    value = TextField(help_text="String value of most CF types")
    path = TextField(help_text="(required) read preferences from a plist")  # {'required': True}

    class Meta:
        table_name = "plist"
