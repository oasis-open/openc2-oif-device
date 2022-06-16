"""
OSQuery app_schemes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class AppSchemes(BaseModel):
    """
    OS X application schemes and handlers (e.g., http, file, mailto).
    """
    scheme = TextField(help_text="Name of the scheme/protocol")
    handler = TextField(help_text="Application label for the handler")
    enabled = IntegerField(help_text="1 if this handler is the OS default, else 0")
    external = IntegerField(help_text="1 if this handler does NOT exist on OS X by default, else 0")
    protected = IntegerField(help_text="1 if this handler is protected (reserved) by OS X, else 0")

    class Meta:
        table_name = "app_schemes"
