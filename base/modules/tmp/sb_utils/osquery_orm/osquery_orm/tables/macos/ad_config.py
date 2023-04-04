"""
OSQuery ad_config ORM
"""
from ...orm import BaseModel
from peewee import TextField


class AdConfig(BaseModel):
    """
    OS X Active Directory configuration.
    """
    name = TextField(help_text="The OS X-specific configuration name")
    domain = TextField(help_text="Active Directory trust domain")
    option = TextField(help_text="Canonical name of option")
    value = TextField(help_text="Variable typed option value")

    class Meta:
        table_name = "ad_config"
