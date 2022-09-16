"""
OSQuery usb_devices ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class UsbDevices(BaseModel):
    """
    USB devices that are actively plugged into the host system.
    """
    usb_address = IntegerField(help_text="USB Device used address")
    usb_port = IntegerField(help_text="USB Device used port")
    vendor = TextField(help_text="USB Device vendor string")
    vendor_id = TextField(help_text="Hex encoded USB Device vendor identifier")
    version = TextField(help_text="USB Device version number")
    model = TextField(help_text="USB Device model string")
    model_id = TextField(help_text="Hex encoded USB Device model identifier")
    serial = TextField(help_text="USB Device serial connection")
    class_ = TextField(help_text="USB Device class", column_name="class")
    subclass = TextField(help_text="USB Device subclass")
    protocol = TextField(help_text="USB Device protocol")
    removable = IntegerField(help_text="1 If USB device is removable else 0")

    class Meta:
        table_name = "usb_devices"
