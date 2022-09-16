"""
OSQuery intel_me_info ORM
"""
from ...orm import BaseModel
from peewee import TextField


class IntelMeInfo(BaseModel):
    """
    Intel ME/CSE Info.
    """
    version = TextField(help_text="Intel ME version")

    class Meta:
        table_name = "intel_me_info"
