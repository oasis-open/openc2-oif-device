"""
OSQuery etc_hosts ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class EtcHosts(BaseModel):
    """
    Line-parsed /etc/hosts.
    """
    address = TextField(help_text="IP address mapping")
    hostnames = TextField(help_text="Raw hosts mapping")

    class Meta:
        table_name = "etc_hosts"


# OS specific properties for Linux
class Linux_EtcHosts(EtcHosts):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "etc_hosts"
