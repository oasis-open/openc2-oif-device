"""
OSQuery hardware_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class HardwareEvents(BaseModel):
    """
    Hardware (PCI/USB/HID) events from UDEV or IOKit.
    """
    action = TextField(help_text="Remove, insert, change properties, etc")
    path = TextField(help_text="Local device path assigned (optional)")
    type = TextField(help_text="Type of hardware and hardware event")
    driver = TextField(help_text="Driver claiming the device")
    vendor = TextField(help_text="Hardware device vendor")
    vendor_id = TextField(help_text="Hex encoded Hardware vendor identifier")
    model = TextField(help_text="Hardware device model")
    model_id = TextField(help_text="Hex encoded Hardware model identifier")
    serial = TextField(help_text="Device serial (optional)")
    revision = TextField(help_text="Device revision (optional)")
    time = BigIntegerField(help_text="Time of hardware event")
    eid = TextField(help_text="Event ID")  # {'hidden': True}

    class Meta:
        table_name = "hardware_events"
