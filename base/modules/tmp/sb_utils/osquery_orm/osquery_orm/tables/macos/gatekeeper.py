"""
OSQuery gatekeeper ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class Gatekeeper(BaseModel):
    """
    OS X Gatekeeper Details.
    """
    assessments_enabled = IntegerField(help_text="1 If a Gatekeeper is enabled else 0")
    dev_id_enabled = IntegerField(help_text="1 If a Gatekeeper allows execution from identified developers else 0")
    version = TextField(help_text="Version of Gatekeeper\'s gke.bundle")
    opaque_version = TextField(help_text="Version of Gatekeeper\'s gkopaque.bundle")

    class Meta:
        table_name = "gatekeeper"
