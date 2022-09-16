"""
OSQuery iptables ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class Iptables(BaseModel):
    """
    Linux IP packet filtering and NAT tool.
    """
    filter_name = TextField(help_text="Packet matching filter table name.")
    chain = TextField(help_text="Size of module content.")
    policy = TextField(help_text="Policy that applies for this rule.")
    target = TextField(help_text="Target that applies for this rule.")
    protocol = IntegerField(help_text="Protocol number identification.")
    src_port = TextField(help_text="Protocol source port(s).")
    dst_port = TextField(help_text="Protocol destination port(s).")
    src_ip = TextField(help_text="Source IP address.")
    src_mask = TextField(help_text="Source IP address mask.")
    iniface = TextField(help_text="Input interface for the rule.")
    iniface_mask = TextField(help_text="Input interface mask for the rule.")
    dst_ip = TextField(help_text="Destination IP address.")
    dst_mask = TextField(help_text="Destination IP address mask.")
    outiface = TextField(help_text="Output interface for the rule.")
    outiface_mask = TextField(help_text="Output interface mask for the rule.")
    match = TextField(help_text="Matching rule that applies.")
    packets = IntegerField(help_text="Number of matching packets for this rule.")
    bytes = IntegerField(help_text="Number of matching bytes for this rule.")

    class Meta:
        table_name = "iptables"
