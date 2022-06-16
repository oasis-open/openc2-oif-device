"""
OSQuery preferences ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Preferences(BaseModel):
    """
    OS X defaults and managed preferences.
    Examples:
        select * from preferences where domain = 'loginwindow'
        select preferences.* from users join preferences using (username)
    """
    domain = TextField(help_text="Application ID usually in com.name.product format")  # {'index': True}
    key = TextField(help_text="Preference top-level key")  # {'index': True}
    subkey = TextField(help_text="Intemediate key path, includes lists/dicts")
    value = TextField(help_text="String value of most CF types")
    forced = IntegerField(help_text="1 if the value is forced/managed, else 0")
    username = TextField(help_text="(optional) read preferences for a specific user")  # {'additional': True}
    host = TextField(help_text="\'current\' or \'any\' host, where \'current\' takes precedence")

    class Meta:
        table_name = "preferences"
