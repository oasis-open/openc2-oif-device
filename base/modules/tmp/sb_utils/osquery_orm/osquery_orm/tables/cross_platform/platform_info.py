"""
OSQuery platform_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class PlatformInfo(BaseModel):
    """
    Information about EFI/UEFI/ROM and platform/boot.
    """
    vendor = TextField(help_text="Platform code vendor")
    version = TextField(help_text="Platform code version")
    date = TextField(help_text="Self-reported platform code update date")
    revision = TextField(help_text="BIOS major and minor revision")
    address = TextField(help_text="Relative address of firmware mapping")
    size = TextField(help_text="Size in bytes of firmware")
    volume_size = IntegerField(help_text="(Optional) size of firmware volume")
    extra = TextField(help_text="Platform-specific additional information")

    class Meta:
        table_name = "platform_info"
