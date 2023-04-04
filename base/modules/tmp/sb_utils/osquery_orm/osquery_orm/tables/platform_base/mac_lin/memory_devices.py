"""
OSQuery memory_devices ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class MemoryDevices(BaseModel):
    """
    Physical memory device (type 17) information retrieved from SMBIOS.
    """
    handle = TextField(help_text="Handle, or instance number, associated with the structure in SMBIOS")
    array_handle = TextField(help_text="The memory array that the device is attached to")
    form_factor = TextField(help_text="Implementation form factor for this memory device")
    total_width = IntegerField(help_text="Total width, in bits, of this memory device, including any check or error-correction bits")
    data_width = IntegerField(help_text="Data width, in bits, of this memory device")
    size = IntegerField(help_text="Size of memory device in Megabyte")
    set = IntegerField(help_text="Identifies if memory device is one of a set of devices.  A value of 0 indicates no set affiliation.")
    device_locator = TextField(help_text="String number of the string that identifies the physically-labeled socket or board position where the memory device is located")
    bank_locator = TextField(help_text="String number of the string that identifies the physically-labeled bank where the memory device is located")
    memory_type = TextField(help_text="Type of memory used")
    memory_type_details = TextField(help_text="Additional details for memory device")
    max_speed = IntegerField(help_text="Max speed of memory device in megatransfers per second (MT/s)")
    configured_clock_speed = IntegerField(help_text="Configured speed of memory device in megatransfers per second (MT/s)")
    manufacturer = TextField(help_text="Manufacturer ID string")
    serial_number = TextField(help_text="Serial number of memory device")
    asset_tag = TextField(help_text="Manufacturer specific asset tag of memory device")
    part_number = TextField(help_text="Manufacturer specific serial number of memory device")
    min_voltage = IntegerField(help_text="Minimum operating voltage of device in millivolts")
    max_voltage = IntegerField(help_text="Maximum operating voltage of device in millivolts")
    configured_voltage = IntegerField(help_text="Configured operating voltage of device in millivolts")

    class Meta:
        table_name = "memory_devices"
