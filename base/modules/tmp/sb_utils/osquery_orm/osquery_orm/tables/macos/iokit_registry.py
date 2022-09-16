"""
OSQuery iokit_registry ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class IokitRegistry(BaseModel):
    """
    The full IOKit registry without selecting a plane.
    """
    name = TextField(help_text="Default name of the node")
    class_ = TextField(help_text="Best matching device class (most-specific category)", column_name="class")
    id = BigIntegerField(help_text="IOKit internal registry ID")
    parent = BigIntegerField(help_text="Parent registry ID")
    busy_state = IntegerField(help_text="1 if the node is in a busy state else 0")
    retain_count = IntegerField(help_text="The node reference count")
    depth = IntegerField(help_text="Node nested depth")

    class Meta:
        table_name = "iokit_registry"
