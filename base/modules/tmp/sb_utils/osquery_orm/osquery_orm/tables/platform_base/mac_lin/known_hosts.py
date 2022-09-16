"""
OSQuery known_hosts ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, TextField
from ...cross_platform import Users


class KnownHosts(BaseModel):
    """
    A line-delimited known_hosts table.
    Examples:
        select * from users join known_hosts using (uid)
    """
    uid = BigIntegerField(help_text="The local user that owns the known_hosts file")  # {'index': True}
    key = TextField(help_text="parsed authorized keys line")
    key_file = TextField(help_text="Path to known_hosts file")
    known_hosts = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "known_hosts"
