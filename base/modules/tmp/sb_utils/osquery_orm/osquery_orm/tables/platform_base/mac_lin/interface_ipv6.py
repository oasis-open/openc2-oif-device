"""
OSQuery interface_ipv6 ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class InterfaceIpv6(BaseModel):
    """
    IPv6 configuration and stats of network interfaces.
    """
    interface = TextField(help_text="Interface name")
    hop_limit = IntegerField(help_text="Current Hop Limit")
    forwarding_enabled = IntegerField(help_text="Enable IP forwarding")
    redirect_accept = IntegerField(help_text="Accept ICMP redirect messages")
    rtadv_accept = IntegerField(help_text="Accept ICMP Router Advertisement")

    class Meta:
        table_name = "interface_ipv6"
