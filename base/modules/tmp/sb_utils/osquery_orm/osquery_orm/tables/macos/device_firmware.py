"""
OSQuery device_firmware ORM
"""
from ...orm import BaseModel
from peewee import TextField


class DeviceFirmware(BaseModel):
    """
    A best-effort list of discovered firmware versions.
    """
    type = TextField(help_text="Type of device")
    device = TextField(help_text="The device name")  # {'index': True}
    version = TextField(help_text="Firmware version")

    class Meta:
        table_name = "device_firmware"
