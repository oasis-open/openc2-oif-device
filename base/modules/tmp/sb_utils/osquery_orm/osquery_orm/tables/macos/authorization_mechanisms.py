"""
OSQuery authorization_mechanisms ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class AuthorizationMechanisms(BaseModel):
    """
    OS X Authorization mechanisms database.
    Examples:
        select * from authorization_mechanisms;
        select * from authorization_mechanisms where label = 'system.login.console';
        select * from authorization_mechanisms where label = 'authenticate';
    """
    label = TextField(help_text="Label of the authorization right")  # {'index': True}
    plugin = TextField(help_text="Authorization plugin name")
    mechanism = TextField(help_text="Name of the mechanism that will be called")
    privileged = TextField(help_text="If privileged it will run as root, else as an anonymous user")
    entry = TextField(help_text="The whole string entry")

    class Meta:
        table_name = "authorization_mechanisms"
