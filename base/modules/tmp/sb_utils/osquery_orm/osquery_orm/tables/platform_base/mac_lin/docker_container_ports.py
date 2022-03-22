"""
OSQuery docker_container_ports ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class DockerContainerPorts(BaseModel):
    """
    Docker container ports.
    Examples:
        select * from docker_container_ports
        select * from docker_container_ports where id = '1234567890abcdef'
        select * from docker_container_ports where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Container ID")  # {'additional': True}
    type = TextField(help_text="Protocol (tcp, udp)")
    port = IntegerField(help_text="Port inside the container")
    host_ip = TextField(help_text="Host IP address on which public port is listening")
    host_port = IntegerField(help_text="Host port")

    class Meta:
        table_name = "docker_container_ports"
