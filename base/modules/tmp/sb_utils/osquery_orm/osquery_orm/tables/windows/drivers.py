"""
OSQuery drivers ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Drivers(BaseModel):
    """
    Details for in-use Windows device drivers. This does not display installed but unused drivers.
    Examples:
        select * from drivers
    """
    device_id = TextField(help_text="Device ID")
    device_name = TextField(help_text="Device name")
    image = TextField(help_text="Path to driver image file")
    description = TextField(help_text="Driver description")
    service = TextField(help_text="Driver service name, if one exists")
    service_key = TextField(help_text="Driver service registry key")
    version = TextField(help_text="Driver version")
    inf = TextField(help_text="Associated inf file")
    class_ = TextField(help_text="Device/driver class name", column_name="class")
    provider = TextField(help_text="Driver provider")
    manufacturer = TextField(help_text="Device manufacturer")
    driver_key = TextField(help_text="Driver key")
    date = BigIntegerField(help_text="Driver date")
    signed = IntegerField(help_text="Whether the driver is signed or not")

    class Meta:
        table_name = "drivers"
