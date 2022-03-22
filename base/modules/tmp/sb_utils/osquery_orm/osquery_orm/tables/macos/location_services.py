"""
OSQuery location_services ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField


class LocationServices(BaseModel):
    """
    Reports the status of the Location Services feature of the OS.
    """
    enabled = IntegerField(help_text="1 if Location Services are enabled, else 0")

    class Meta:
        table_name = "location_services"
