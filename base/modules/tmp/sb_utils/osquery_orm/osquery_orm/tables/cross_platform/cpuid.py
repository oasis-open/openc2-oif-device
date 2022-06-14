"""
OSQuery cpuid ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Cpuid(BaseModel):
    """
    Useful CPU features from the cpuid ASM call.
    """
    feature = TextField(help_text="Present feature flags")
    value = TextField(help_text="Bit value or string")
    output_register = TextField(help_text="Register used to for feature value")
    output_bit = IntegerField(help_text="Bit in register value for feature value")
    input_eax = TextField(help_text="Value of EAX used")

    class Meta:
        table_name = "cpuid"
