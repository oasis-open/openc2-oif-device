"""
OSQuery power_sensors ORM
"""
from osquery_orm.orm import BaseModel
from peewee import ForeignKeyField, TextField
from .smc_keys import SmcKeys


class PowerSensors(BaseModel):
    """
    Machine power (currents, voltages, wattages, etc) sensors.
    Examples:
        select * from power_sensors where category = 'voltage'
    """
    key = TextField(help_text="The SMC key on OS X")  # {'index': True}
    category = TextField(help_text="The sensor category: currents, voltage, wattage")
    name = TextField(help_text="Name of power source")
    value = TextField(help_text="Power in Watts")
    power_sensors = ForeignKeyField(SmcKeys, backref='key')

    class Meta:
        table_name = "power_sensors"
