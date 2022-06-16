"""
OSQuery interface_details ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class InterfaceDetails(BaseModel):
    """
    Detailed information and stats of network interfaces.
    Examples:
        select interface, mac, type, idrops as input_drops from interface_details;
        select interface, mac, type, flags, (1<<8) as promisc_flag from interface_details where (flags & promisc_flag) > 0;
        select interface, mac, type, flags, (1<<3) as loopback_flag from interface_details where (flags & loopback_flag) > 0;
    """
    interface = TextField(help_text="Interface name")
    mac = TextField(help_text="MAC of interface (optional)")
    type = IntegerField(help_text="Interface type (includes virtual)")
    mtu = IntegerField(help_text="Network MTU")
    metric = IntegerField(help_text="Metric based on the speed of the interface")
    flags = IntegerField(help_text="Flags (netdevice) for the device")
    ipackets = BigIntegerField(help_text="Input packets")
    opackets = BigIntegerField(help_text="Output packets")
    ibytes = BigIntegerField(help_text="Input bytes")
    obytes = BigIntegerField(help_text="Output bytes")
    ierrors = BigIntegerField(help_text="Input errors")
    oerrors = BigIntegerField(help_text="Output errors")
    idrops = BigIntegerField(help_text="Input drops")
    odrops = BigIntegerField(help_text="Output drops")
    collisions = BigIntegerField(help_text="Packet Collisions detected")
    last_change = BigIntegerField(help_text="Time of last device modification (optional)")

    class Meta:
        table_name = "interface_details"


# OS specific properties for Posix
class Posix_InterfaceDetails(InterfaceDetails):
    link_speed = BigIntegerField(help_text="Interface speed in Mb/s")

    class Meta:
        table_name = "interface_details"


# OS specific properties for Linux
class Linux_InterfaceDetails(InterfaceDetails):
    pci_slot = TextField(help_text="PCI slot number")

    class Meta:
        table_name = "interface_details"


# OS specific properties for Windows
class Windows_InterfaceDetails(InterfaceDetails):
    friendly_name = TextField(help_text="The friendly display name of the interface.")
    description = TextField(help_text="Short description of the object a one-line string.")
    manufacturer = TextField(help_text="Name of the network adapter\'s manufacturer.")
    connection_id = TextField(help_text="Name of the network connection as it appears in the Network Connections Control Panel program.")
    connection_status = TextField(help_text="State of the network adapter connection to the network.")
    enabled = IntegerField(help_text="Indicates whether the adapter is enabled or not.")
    physical_adapter = IntegerField(help_text="Indicates whether the adapter is a physical or a logical adapter.")
    speed = IntegerField(help_text="Estimate of the current bandwidth in bits per second.")
    service = TextField(help_text="The name of the service the network adapter uses.")
    dhcp_enabled = IntegerField(help_text="If TRUE, the dynamic host configuration protocol (DHCP) server automatically assigns an IP address to the computer system when establishing a network connection.")
    dhcp_lease_expires = TextField(help_text="Expiration date and time for a leased IP address that was assigned to the computer by the dynamic host configuration protocol (DHCP) server.")
    dhcp_lease_obtained = TextField(help_text="Date and time the lease was obtained for the IP address assigned to the computer by the dynamic host configuration protocol (DHCP) server.")
    dhcp_server = TextField(help_text="IP address of the dynamic host configuration protocol (DHCP) server.")
    dns_domain = TextField(help_text="Organization name followed by a period and an extension that indicates the type of organization, such as \'microsoft.com\'.")
    dns_domain_suffix_search_order = TextField(help_text="Array of DNS domain suffixes to be appended to the end of host names during name resolution.")
    dns_host_name = TextField(help_text="Host name used to identify the local computer for authentication by some utilities.")
    dns_server_search_order = TextField(help_text="Array of server IP addresses to be used in querying for DNS servers.")

    class Meta:
        table_name = "interface_details"
