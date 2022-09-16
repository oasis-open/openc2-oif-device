"""
OSQuery arp_cache ORM
"""
from ...orm import BaseModel
from peewee import TextField


class ArpCache(BaseModel):
    """
    Address resolution cache, both static and dynamic (from ARP, NDP).
    """
    address = TextField(help_text="IPv4 address target")
    mac = TextField(help_text="MAC address of broadcasted address")
    interface = TextField(help_text="Interface of the network for the MAC")
    permanent = TextField(help_text="1 for true, 0 for false")

    class Meta:
        table_name = "arp_cache"
