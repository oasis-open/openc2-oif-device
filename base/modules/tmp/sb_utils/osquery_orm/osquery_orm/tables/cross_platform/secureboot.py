"""
OSQuery secureboot ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField


class Secureboot(BaseModel):
    """
    Secure Boot UEFI Settings.
    """
    secure_boot = IntegerField(help_text="Whether secure boot is enabled")
    setup_mode = IntegerField(help_text="Whether setup mode is enabled")

    class Meta:
        table_name = "secureboot"
