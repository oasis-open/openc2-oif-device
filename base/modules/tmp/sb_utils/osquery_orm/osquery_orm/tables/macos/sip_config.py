"""
OSQuery sip_config ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class SipConfig(BaseModel):
    """
    Apple\'s System Integrity Protection (rootless) status.
    Examples:
        select * from sip_config
    """
    config_flag = TextField(help_text="The System Integrity Protection config flag")
    enabled = IntegerField(help_text="1 if this configuration is enabled, otherwise 0")
    enabled_nvram = IntegerField(help_text="1 if this configuration is enabled, otherwise 0")

    class Meta:
        table_name = "sip_config"
