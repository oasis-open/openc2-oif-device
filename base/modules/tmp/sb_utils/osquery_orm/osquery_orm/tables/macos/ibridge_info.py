"""
OSQuery ibridge_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class IbridgeInfo(BaseModel):
    """
    Information about the Apple iBridge hardware controller.
    """
    boot_uuid = TextField(help_text="Boot UUID of the iBridge controller")
    coprocessor_version = TextField(help_text="The manufacturer and chip version")
    firmware_version = TextField(help_text="The build version of the firmware")
    unique_chip_id = TextField(help_text="Unique id of the iBridge controller")

    class Meta:
        table_name = "ibridge_info"
