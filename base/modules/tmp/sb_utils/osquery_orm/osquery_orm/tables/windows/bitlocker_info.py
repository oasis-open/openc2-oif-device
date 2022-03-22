"""
OSQuery bitlocker_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class BitlockerInfo(BaseModel):
    """
    Retrieve bitlocker status of the machine.
    """
    device_id = TextField(help_text="ID of the encrypted drive.")
    drive_letter = TextField(help_text="Drive letter of the encrypted drive.")
    persistent_volume_id = TextField(help_text="Persistent ID of the drive.")
    conversion_status = IntegerField(help_text="The bitlocker conversion status of the drive.")
    protection_status = IntegerField(help_text="The bitlocker protection status of the drive.")
    encryption_method = TextField(help_text="The encryption type of the device.")
    version = IntegerField(help_text="The FVE metadata version of the drive.")
    percentage_encrypted = IntegerField(help_text="The percentage of the drive that is encrypted.")
    lock_status = IntegerField(help_text="The accessibility status of the drive from Windows.")

    class Meta:
        table_name = "bitlocker_info"
