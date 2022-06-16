"""
OSQuery wmi_bios_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class WmiBiosInfo(BaseModel):
    """
    Lists important information from the system bios.
    Examples:
        select * from wmi_bios_info
        select * from wmi_bios_info where name = 'AMTControl'
    """
    name = TextField(help_text="Name of the Bios setting")
    value = TextField(help_text="Value of the Bios setting")

    class Meta:
        table_name = "wmi_bios_info"
