"""
OSQuery docker_container_networks ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class DockerContainerNetworks(BaseModel):
    """
    Docker container networks.
    Examples:
        select * from docker_container_networks
        select * from docker_container_networks where id = '1234567890abcdef'
        select * from docker_container_networks where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'index': True}
    name = TextField(help_text="Network name")  # {'index': True}
    network_id = TextField(help_text="Network ID")
    endpoint_id = TextField(help_text="Endpoint ID")
    gateway = TextField(help_text="Gateway")
    ip_address = TextField(help_text="IP address")
    ip_prefix_len = IntegerField(help_text="IP subnet prefix length")
    ipv6_gateway = TextField(help_text="IPv6 gateway")
    ipv6_address = TextField(help_text="IPv6 address")
    ipv6_prefix_len = IntegerField(help_text="IPv6 subnet prefix length")
    mac_address = TextField(help_text="MAC address")

    class Meta:
        table_name = "docker_container_networks"
