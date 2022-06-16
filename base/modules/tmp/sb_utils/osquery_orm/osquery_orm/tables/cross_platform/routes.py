"""
OSQuery routes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Routes(BaseModel):
    """
    The active route table for the host system.
    """
    destination = TextField(help_text="Destination IP address")
    netmask = IntegerField(help_text="Netmask length")
    gateway = TextField(help_text="Route gateway")
    source = TextField(help_text="Route source")
    flags = IntegerField(help_text="Flags to describe route")
    interface = TextField(help_text="Route local interface")
    mtu = IntegerField(help_text="Maximum Transmission Unit for the route")
    metric = IntegerField(help_text="Cost of route. Lowest is preferred")
    type = TextField(help_text="Type of route")  # {'additional': True}

    class Meta:
        table_name = "routes"


# OS specific properties for Posix
class Posix_Routes(Routes):
    hopcount = IntegerField(help_text="Max hops expected")

    class Meta:
        table_name = "routes"
