"""
OSQuery kernel_info ORM
"""
from ...orm import BaseModel
from peewee import TextField


class KernelInfo(BaseModel):
    """
    Basic active kernel information.
    """
    version = TextField(help_text="Kernel version")
    arguments = TextField(help_text="Kernel arguments")
    path = TextField(help_text="Kernel path")
    device = TextField(help_text="Kernel device identifier")

    class Meta:
        table_name = "kernel_info"
