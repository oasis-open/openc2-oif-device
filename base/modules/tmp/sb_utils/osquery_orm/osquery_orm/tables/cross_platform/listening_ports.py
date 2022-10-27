"""
OSQuery listening_ports ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from .etc_protocols import EtcProtocols
from ..consts import SocketFamily


class ListeningPorts(BaseModel):
    """
    Processes with listening (bound) network sockets/ports.
    """
    pid = IntegerField(help_text="Process (or thread) ID")
    port = IntegerField(help_text="Transport layer port")
    # protocol = IntegerField(help_text="Transport protocol (TCP/UDP)")
    protocol = ForeignKeyField(EtcProtocols, EtcProtocols.number, column_name="protocol", help_text="Transport protocol (TCP/UDP)")
    # family = IntegerField(help_text="Network protocol (IPv4, IPv6)")
    family = IntegerField(choices=SocketFamily, help_text="Network protocol (IPv4, IPv6)")
    address = TextField(help_text="Specific address for bind")
    fd = BigIntegerField(help_text="Socket file descriptor number")
    socket = BigIntegerField(help_text="Socket handle or inode number")
    path = TextField(help_text="Path for UNIX domain sockets")

    class Meta:
        table_name = "listening_ports"


# OS specific properties for Linux
class Linux_ListeningPorts(ListeningPorts):
    net_namespace = TextField(help_text="The inode number of the network namespace")

    class Meta:
        table_name = "listening_ports"
