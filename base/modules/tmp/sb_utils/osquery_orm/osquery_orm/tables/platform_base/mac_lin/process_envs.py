"""
OSQuery process_envs ORM
"""
from ....orm import BaseModel
from peewee import IntegerField, TextField


class ProcessEnvs(BaseModel):
    """
    A key/value table of environment variables for each process.
    Examples:
        select * from process_envs where pid = 1
        select pe.*
             from process_envs pe, (select * from processes limit 10) p
             where p.pid = pe.pid;
    """
    pid = IntegerField(help_text="Process (or thread) ID")  # {'index': True}
    key = TextField(help_text="Environment variable name")
    value = TextField(help_text="Environment variable value")

    class Meta:
        table_name = "process_envs"
