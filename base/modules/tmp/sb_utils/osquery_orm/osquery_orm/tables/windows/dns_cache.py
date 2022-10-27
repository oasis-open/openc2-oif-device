"""
OSQuery dns_cache ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class DnsCache(BaseModel):
    """
    Enumerate the DNS cache using the undocumented DnsGetCacheDataTable function in dnsapi.dll.
    Examples:
        select * from dns_cache
    """
    name = TextField(help_text="DNS record name")
    type = TextField(help_text="DNS record type")
    flags = IntegerField(help_text="DNS record flags")

    class Meta:
        table_name = "dns_cache"
