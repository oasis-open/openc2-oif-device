"""
OSQuery sandboxes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Sandboxes(BaseModel):
    """
    OS X application sandboxes container details.
    """
    label = TextField(help_text="UTI-format bundle or label ID")
    user = TextField(help_text="Sandbox owner")
    enabled = IntegerField(help_text="Application sandboxings enabled on container")
    build_id = TextField(help_text="Sandbox-specific identifier")
    bundle_path = TextField(help_text="Application bundle used by the sandbox")
    path = TextField(help_text="Path to sandbox container directory")

    class Meta:
        table_name = "sandboxes"
