"""
OSQuery alf ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Alf(BaseModel):
    """
    OS X application layer firewall (ALF) service details.
    """
    allow_signed_enabled = IntegerField(help_text="1 If allow signed mode is enabled else 0")
    firewall_unload = IntegerField(help_text="1 If firewall unloading enabled else 0")
    global_state = IntegerField(help_text="1 If the firewall is enabled with exceptions, 2 if the firewall is configured to block all incoming connections, else 0")
    logging_enabled = IntegerField(help_text="1 If logging mode is enabled else 0")
    logging_option = IntegerField(help_text="Firewall logging option")
    stealth_enabled = IntegerField(help_text="1 If stealth mode is enabled else 0")
    version = TextField(help_text="Application Layer Firewall version")

    class Meta:
        table_name = "alf"
