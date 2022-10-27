"""
OSQuery shell_history ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from ...cross_platform import Users


class ShellHistory(BaseModel):
    """
    A line-delimited (command) table of per-user .*_history data.
    Examples:
        select * from users join shell_history using (uid)
    """
    uid = BigIntegerField(help_text="Shell history owner")  # {'additional': True}
    time = IntegerField(help_text="Entry timestamp. It could be absent, default value is 0.")
    command = TextField(help_text="Unparsed date/line/command history line")
    history_file = TextField(help_text="Path to the .*_history for this user")
    shell_history = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "shell_history"
