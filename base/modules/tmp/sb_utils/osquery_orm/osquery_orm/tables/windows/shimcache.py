"""
OSQuery shimcache ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class Shimcache(BaseModel):
    """
    Application Compatibility Cache, contains artifacts of execution.
    Examples:
        select * from shimcache;
    """
    entry = IntegerField(help_text="Execution order.")
    path = TextField(help_text="This is the path to the executed file.")
    modified_time = IntegerField(help_text="File Modified time.")
    execution_flag = IntegerField(help_text="Boolean Execution flag, 1 for execution, 0 for no execution, -1 for missing (this flag does not exist on Windows 10 and higher).")

    class Meta:
        table_name = "shimcache"
