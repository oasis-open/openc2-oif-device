"""
OSQuery fan_speed_sensors ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class FanSpeedSensors(BaseModel):
    """
    Fan speeds.
    """
    fan = TextField(help_text="Fan number")
    name = TextField(help_text="Fan name")
    actual = IntegerField(help_text="Actual speed")
    min = IntegerField(help_text="Minimum speed")
    max = IntegerField(help_text="Maximum speed")
    target = IntegerField(help_text="Target speed")

    class Meta:
        table_name = "fan_speed_sensors"
