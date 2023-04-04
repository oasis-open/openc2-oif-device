"""
OSQuery dns_resolvers ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DnsResolvers(BaseModel):
    """
    Resolvers used by this host.
    """
    id = IntegerField(help_text="Address type index or order")
    type = TextField(help_text="Address type: sortlist, nameserver, search")
    address = TextField(help_text="Resolver IP/IPv6 address")
    netmask = TextField(help_text="Address (sortlist) netmask length")
    options = BigIntegerField(help_text="Resolver options")

    class Meta:
        table_name = "dns_resolvers"


# OS specific properties for Linux
class Linux_DnsResolvers(DnsResolvers):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "dns_resolvers"
