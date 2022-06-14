"""
OSQuery interface_addresses ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class InterfaceAddresses(BaseModel):
    """
    Network interfaces and relevant metadata.
    """
    interface = TextField(help_text="Interface name")
    address = TextField(help_text="Specific address for interface")
    mask = TextField(help_text="Interface netmask")
    broadcast = TextField(help_text="Broadcast address for the interface")
    point_to_point = TextField(help_text="PtP address for the interface")
    type = TextField(help_text="Type of address. One of dhcp, manual, auto, other, unknown")

    class Meta:
        table_name = "interface_addresses"


# OS specific properties for Windows
class Windows_InterfaceAddresses(InterfaceAddresses):
    friendly_name = TextField(help_text="The friendly display name of the interface.")

    class Meta:
        table_name = "interface_addresses"
