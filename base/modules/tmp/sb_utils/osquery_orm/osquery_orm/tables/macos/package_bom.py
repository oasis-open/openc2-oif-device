"""
OSQuery package_bom ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class PackageBom(BaseModel):
    """
    OS X package bill of materials (BOM) file list.
    Examples:
        select * from package_bom where path = '/var/db/receipts/com.apple.pkg.MobileDevice.bom'
    """
    filepath = TextField(help_text="Package file or directory")
    uid = IntegerField(help_text="Expected user of file or directory")
    gid = IntegerField(help_text="Expected group of file or directory")
    mode = IntegerField(help_text="Expected permissions")
    size = BigIntegerField(help_text="Expected file size")
    modified_time = IntegerField(help_text="Timestamp the file was installed")
    path = TextField(help_text="Path of package bom")  # {'required': True}

    class Meta:
        table_name = "package_bom"
