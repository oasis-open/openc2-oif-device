"""
OSQuery load_average ORM
"""
from ....orm import BaseModel
from peewee import TextField


class LoadAverage(BaseModel):
    """
    Displays information about the system wide load averages.
    Examples:
        select * from load_average;
    """
    period = TextField(help_text="Period over which the average is calculated.")
    average = TextField(help_text="Load average over the specified period.")

    class Meta:
        table_name = "load_average"
