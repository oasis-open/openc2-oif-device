"""
OSQuery kernel_modules ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class KernelModules(BaseModel):
    """
    Linux kernel modules both loaded and within the load search path.
    """
    name = TextField(help_text="Module name")
    size = BigIntegerField(help_text="Size of module content")
    used_by = TextField(help_text="Module reverse dependencies")
    status = TextField(help_text="Kernel module status")
    address = TextField(help_text="Kernel module address")

    class Meta:
        table_name = "kernel_modules"
