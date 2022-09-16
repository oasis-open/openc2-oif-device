"""
OSQuery system_info ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class SystemInfo(BaseModel):
    """
    System information for identification.
    """
    hostname = TextField(help_text="Network hostname including domain")
    uuid = TextField(help_text="Unique ID provided by the system")
    cpu_type = TextField(help_text="CPU type")
    cpu_subtype = TextField(help_text="CPU subtype")
    cpu_brand = TextField(help_text="CPU brand string, contains vendor and model")
    cpu_physical_cores = IntegerField(help_text="Number of physical CPU cores in to the system")
    cpu_logical_cores = IntegerField(help_text="Number of logical CPU cores available to the system")
    cpu_microcode = TextField(help_text="Microcode version")
    physical_memory = BigIntegerField(help_text="Total physical memory in bytes")
    hardware_vendor = TextField(help_text="Hardware vendor")
    hardware_model = TextField(help_text="Hardware model")
    hardware_version = TextField(help_text="Hardware version")
    hardware_serial = TextField(help_text="Device serial number")
    board_vendor = TextField(help_text="Board vendor")
    board_model = TextField(help_text="Board model")
    board_version = TextField(help_text="Board version")
    board_serial = TextField(help_text="Board serial number")
    computer_name = TextField(help_text="Friendly computer name (optional)")
    local_hostname = TextField(help_text="Local hostname (optional)")

    class Meta:
        table_name = "system_info"
