"""
OSQuery temperature_sensors ORM
"""
from osquery_orm.orm import BaseModel
from peewee import DoubleField, ForeignKeyField, TextField
from .smc_keys import SmcKeys


class TemperatureSensors(BaseModel):
    """
    Machine\'s temperature sensors.
    """
    key = TextField(help_text="The SMC key on OS X")  # {'index': True}
    name = TextField(help_text="Name of temperature source")
    celsius = DoubleField(help_text="Temperature in Celsius")
    fahrenheit = DoubleField(help_text="Temperature in Fahrenheit")
    temperature_sensors = ForeignKeyField(SmcKeys, backref='key')

    class Meta:
        table_name = "temperature_sensors"
