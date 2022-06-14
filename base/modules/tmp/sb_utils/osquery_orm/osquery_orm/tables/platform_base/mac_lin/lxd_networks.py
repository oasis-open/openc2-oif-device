"""
OSQuery lxd_networks ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class LxdNetworks(BaseModel):
    """
    LXD network information.
    Examples:
        select * from lxd_networks
    """
    name = TextField(help_text="Name of the network")
    type = TextField(help_text="Type of network")
    managed = IntegerField(help_text="1 if network created by LXD, 0 otherwise")
    ipv4_address = TextField(help_text="IPv4 address")
    ipv6_address = TextField(help_text="IPv6 address")
    used_by = TextField(help_text="URLs for containers using this network")
    bytes_received = BigIntegerField(help_text="Number of bytes received on this network")
    bytes_sent = BigIntegerField(help_text="Number of bytes sent on this network")
    packets_received = BigIntegerField(help_text="Number of packets received on this network")
    packets_sent = BigIntegerField(help_text="Number of packets sent on this network")
    hwaddr = TextField(help_text="Hardware address for this network")
    state = TextField(help_text="Network status")
    mtu = IntegerField(help_text="MTU size")

    class Meta:
        table_name = "lxd_networks"
