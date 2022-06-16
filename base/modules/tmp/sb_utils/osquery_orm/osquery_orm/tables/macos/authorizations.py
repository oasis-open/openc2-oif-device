"""
OSQuery authorizations ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Authorizations(BaseModel):
    """
    OS X Authorization rights database.
    Examples:
        select * from authorizations;
        select * from authorizations where label = 'system.login.console';
        select * from authorizations where label = 'authenticate';
        select * from authorizations where label = 'system.preferences.softwareupdate';
    """
    label = TextField(help_text="Item name, usually in reverse domain format")  # {'index': True}
    modified = TextField(help_text="Label top-level key")
    allow_root = TextField(help_text="Label top-level key")
    timeout = TextField(help_text="Label top-level key")
    version = TextField(help_text="Label top-level key")
    tries = TextField(help_text="Label top-level key")
    authenticate_user = TextField(help_text="Label top-level key")
    shared = TextField(help_text="Label top-level key")
    comment = TextField(help_text="Label top-level key")
    created = TextField(help_text="Label top-level key")
    class_ = TextField(help_text="Label top-level key", column_name="class")
    session_owner = TextField(help_text="Label top-level key")

    class Meta:
        table_name = "authorizations"
