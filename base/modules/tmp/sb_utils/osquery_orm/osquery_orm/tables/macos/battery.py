"""
OSQuery battery ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class Battery(BaseModel):
    """
    Provides information about the internal battery of a Macbook.
    """
    manufacturer = TextField(help_text="The battery manufacturer\'s name")
    manufacture_date = IntegerField(help_text="The date the battery was manufactured UNIX Epoch")
    model = TextField(help_text="The battery\'s model number")
    serial_number = TextField(help_text="The battery\'s unique serial number")
    cycle_count = IntegerField(help_text="The number of charge/discharge cycles")
    health = TextField(help_text="One of the following: \"Good\" describes a well-performing battery, \"Fair\" describes a functional battery with limited capacity, or \"Poor\" describes a battery that\'s not capable of providing power")
    condition = TextField(help_text="One of the following: \"Normal\" indicates the condition of the battery is within normal tolerances, \"Service Needed\" indicates that the battery should be checked out by a licensed Mac repair service, \"Permanent Failure\" indicates the battery needs replacement")
    state = TextField(help_text="One of the following: \"AC Power\" indicates the battery is connected to an external power source, \"Battery Power\" indicates that the battery is drawing internal power, \"Off Line\" indicates the battery is off-line or no longer connected")
    charging = IntegerField(help_text="1 if the battery is currently being charged by a power source. 0 otherwise")
    charged = IntegerField(help_text="1 if the battery is currently completely charged. 0 otherwise")
    designed_capacity = IntegerField(help_text="The battery\'s designed capacity in mAh")
    max_capacity = IntegerField(help_text="The battery\'s actual capacity when it is fully charged in mAh")
    current_capacity = IntegerField(help_text="The battery\'s current charged capacity in mAh")
    percent_remaining = IntegerField(help_text="The percentage of battery remaining before it is drained")
    amperage = IntegerField(help_text="The battery\'s current amperage in mA")
    voltage = IntegerField(help_text="The battery\'s current voltage in mV")
    minutes_until_empty = IntegerField(help_text="The number of minutes until the battery is fully depleted. This value is -1 if this time is still being calculated")
    minutes_to_full_charge = IntegerField(help_text="The number of minutes until the battery is fully charged. This value is -1 if this time is still being calculated")

    class Meta:
        table_name = "battery"
