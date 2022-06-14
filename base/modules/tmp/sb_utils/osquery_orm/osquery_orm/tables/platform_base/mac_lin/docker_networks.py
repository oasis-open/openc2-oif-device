"""
OSQuery docker_networks ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DockerNetworks(BaseModel):
    """
    Docker networks information.
    Examples:
        select * from docker_networks
        select * from docker_networks where id = 'cfd2ffd49439'
        select * from docker_networks where id = 'cfd2ffd494395b75d77539761df40cde06a2b6b497e0c9c1adc6c5a79539bfad'
    """
    id = TextField(help_text="Network ID")  # {'index': True}
    name = TextField(help_text="Network name")
    driver = TextField(help_text="Network driver")
    created = BigIntegerField(help_text="Time of creation as UNIX time")
    enable_ipv6 = IntegerField(help_text="1 if IPv6 is enabled on this network. 0 otherwise")
    subnet = TextField(help_text="Network subnet")
    gateway = TextField(help_text="Network gateway")

    class Meta:
        table_name = "docker_networks"
