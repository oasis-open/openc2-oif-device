"""
OSQuery appcompat_shims ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class AppcompatShims(BaseModel):
    """
    Application Compatibility shims are a way to persist malware. This table presents the AppCompat Shim information from the registry in a nice format. See http://files.brucon.org/2015/Tomczak_and_Ballenthin_Shims_for_the_Win.pdf for more details.
    Examples:
        select * from appcompat_shims;
    """
    executable = TextField(help_text="Name of the executable that is being shimmed. This is pulled from the registry.")
    path = TextField(help_text="This is the path to the SDB database.")
    description = TextField(help_text="Description of the SDB.")
    install_time = IntegerField(help_text="Install time of the SDB")
    type = TextField(help_text="Type of the SDB database.")
    sdb_id = TextField(help_text="Unique GUID of the SDB.")

    class Meta:
        table_name = "appcompat_shims"
