"""
OSQuery cups_destinations ORM
"""
from ...orm import BaseModel
from peewee import TextField


class CupsDestinations(BaseModel):
    """
    Returns all configured printers.
    """
    name = TextField(help_text="Name of the printer")
    option_name = TextField(help_text="Option name")
    option_value = TextField(help_text="Option value")

    class Meta:
        table_name = "cups_destinations"
