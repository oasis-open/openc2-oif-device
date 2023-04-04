"""
OSQuery etc_services ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class EtcServices(BaseModel):
    """
    Line-parsed /etc/services.
    """
    name = TextField(help_text="Service name")
    port = IntegerField(help_text="Service port number")
    protocol = TextField(help_text="Transport protocol (TCP/UDP)")
    aliases = TextField(help_text="Optional space separated list of other names for a service")
    comment = TextField(help_text="Optional comment for a service.")

    class Meta:
        table_name = "etc_services"
