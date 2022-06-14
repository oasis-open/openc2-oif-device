"""
OSQuery smart_drive_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class SmartDriveInfo(BaseModel):
    """
    Drive information read by SMART controller utilizing autodetect.
    """
    device_name = TextField(help_text="Name of block device")
    disk_id = IntegerField(help_text="Physical slot number of device, only exists when hardware storage controller exists")
    driver_type = TextField(help_text="The explicit device type used to retrieve the SMART information")
    model_family = TextField(help_text="Drive model family")
    device_model = TextField(help_text="Device Model")
    serial_number = TextField(help_text="Device serial number")
    lu_wwn_device_id = TextField(help_text="Device Identifier")
    additional_product_id = TextField(help_text="An additional drive identifier if any")
    firmware_version = TextField(help_text="Drive firmware version")
    user_capacity = TextField(help_text="Bytes of drive capacity")
    sector_sizes = TextField(help_text="Bytes of drive sector sizes")
    rotation_rate = TextField(help_text="Drive RPM")
    form_factor = TextField(help_text="Form factor if reported")
    in_smartctl_db = IntegerField(help_text="Boolean value for if drive is recognized")
    ata_version = TextField(help_text="ATA version of drive")
    transport_type = TextField(help_text="Drive transport type")
    sata_version = TextField(help_text="SATA version, if any")
    read_device_identity_failure = TextField(help_text="Error string for device id read, if any")
    smart_supported = TextField(help_text="SMART support status")
    smart_enabled = TextField(help_text="SMART enabled status")
    packet_device_type = TextField(help_text="Packet device type")
    power_mode = TextField(help_text="Device power mode")
    warnings = TextField(help_text="Warning messages from SMART controller")

    class Meta:
        table_name = "smart_drive_info"
