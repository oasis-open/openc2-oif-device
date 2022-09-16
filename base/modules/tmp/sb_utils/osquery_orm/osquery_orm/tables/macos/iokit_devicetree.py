"""
OSQuery iokit_devicetree ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class IokitDevicetree(BaseModel):
    """
    The IOKit registry matching the DeviceTree plane.
    """
    name = TextField(help_text="Device node name")
    class_ = TextField(help_text="Best matching device class (most-specific category)", column_name="class")
    id = BigIntegerField(help_text="IOKit internal registry ID")
    parent = BigIntegerField(help_text="Parent device registry ID")
    device_path = TextField(help_text="Device tree path")
    service = IntegerField(help_text="1 if the device conforms to IOService else 0")
    busy_state = IntegerField(help_text="1 if the device is in a busy state else 0")
    retain_count = IntegerField(help_text="The device reference count")
    depth = IntegerField(help_text="Device nested depth")

    class Meta:
        table_name = "iokit_devicetree"
