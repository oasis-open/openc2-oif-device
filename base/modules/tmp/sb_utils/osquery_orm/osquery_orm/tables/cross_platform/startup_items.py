"""
OSQuery startup_items ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class StartupItems(BaseModel):
    """
    Applications and binaries set as user/login startup items.
    """
    name = TextField(help_text="Name of startup item")
    path = TextField(help_text="Path of startup item")
    args = TextField(help_text="Arguments provided to startup executable")
    type = TextField(help_text="Startup Item or Login Item")
    source = TextField(help_text="Directory or plist containing startup item")
    status = TextField(help_text="Startup status; either enabled or disabled")
    username = TextField(help_text="The user associated with the startup item")

    class Meta:
        table_name = "startup_items"
