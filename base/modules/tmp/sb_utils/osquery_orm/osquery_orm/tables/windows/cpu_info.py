"""
OSQuery cpu_info ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class CpuInfo(BaseModel):
    """
    Retrieve cpu hardware info of the machine.
    """
    device_id = TextField(help_text="The DeviceID of the CPU.")
    model = TextField(help_text="The model of the CPU.")
    manufacturer = TextField(help_text="The manufacturer of the CPU.")
    processor_type = TextField(help_text="The processor type, such as Central, Math, or Video.")
    availability = TextField(help_text="The availability and status of the CPU.")
    cpu_status = IntegerField(help_text="The current operating status of the CPU.")
    number_of_cores = TextField(help_text="The number of cores of the CPU.")
    logical_processors = IntegerField(help_text="The number of logical processors of the CPU.")
    address_width = TextField(help_text="The width of the CPU address bus.")
    current_clock_speed = IntegerField(help_text="The current frequency of the CPU.")
    max_clock_speed = IntegerField(help_text="The maximum possible frequency of the CPU.")
    socket_designation = TextField(help_text="The assigned socket on the board for the given CPU.")

    class Meta:
        table_name = "cpu_info"
