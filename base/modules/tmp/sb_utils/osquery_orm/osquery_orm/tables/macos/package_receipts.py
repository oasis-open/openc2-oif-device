"""
OSQuery package_receipts ORM
"""
from ...orm import BaseModel
from peewee import DoubleField, TextField


class PackageReceipts(BaseModel):
    """
    OS X package receipt details.
    Examples:
        select * from package_bom where path = '/var/db/receipts/com.apple.pkg.MobileDevice.bom'
    """
    package_id = TextField(help_text="Package domain identifier")
    package_filename = TextField(help_text="Filename of original .pkg file")  # {'index': True, 'hidden': True}
    version = TextField(help_text="Installed package version")
    location = TextField(help_text="Optional relative install path on volume")
    install_time = DoubleField(help_text="Timestamp of install time")
    installer_name = TextField(help_text="Name of installer process")
    path = TextField(help_text="Path of receipt plist")  # {'additional': True}

    class Meta:
        table_name = "package_receipts"
