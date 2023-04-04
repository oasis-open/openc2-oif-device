"""
OSQuery lxd_instance_devices ORM
"""
from ....orm import BaseModel
from peewee import TextField


class LxdInstanceDevices(BaseModel):
    """
    LXD instance devices information.
    Examples:
        select * from lxd_instance_devices where name = 'hello'
    """
    name = TextField(help_text="Instance name")  # {'index': True, 'required': True}
    device = TextField(help_text="Name of the device")
    device_type = TextField(help_text="Device type")
    key = TextField(help_text="Device info param name")
    value = TextField(help_text="Device info param value")

    class Meta:
        table_name = "lxd_instance_devices"
