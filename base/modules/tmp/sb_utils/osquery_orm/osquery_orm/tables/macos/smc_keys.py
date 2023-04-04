"""
OSQuery smc_keys ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class SmcKeys(BaseModel):
    """
    Apple\'s system management controller keys.
    Examples:
        select * from smc_keys where key = 'MOJO'
    """
    key = TextField(help_text="4-character key")  # {'additional': True, 'index': True}
    type = TextField(help_text="SMC-reported type literal type")
    size = IntegerField(help_text="Reported size of data in bytes")
    value = TextField(help_text="A type-encoded representation of the key value")
    hidden = IntegerField(help_text="1 if this key is normally hidden, otherwise 0")

    class Meta:
        table_name = "smc_keys"
