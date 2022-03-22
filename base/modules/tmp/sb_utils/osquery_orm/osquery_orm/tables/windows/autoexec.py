"""
OSQuery autoexec ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Autoexec(BaseModel):
    """
    Aggregate of executables that will automatically execute on the target machine. This is an amalgamation of other tables like services, scheduled_tasks, startup_items and more.
    """
    path = TextField(help_text="Path to the executable")  # {'index': True}
    name = TextField(help_text="Name of the program")
    source = TextField(help_text="Source table of the autoexec item")

    class Meta:
        table_name = "autoexec"
