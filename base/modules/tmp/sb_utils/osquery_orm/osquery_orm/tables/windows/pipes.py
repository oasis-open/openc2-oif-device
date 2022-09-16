"""
OSQuery pipes ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Pipes(BaseModel):
    """
    Named and Anonymous pipes.
    Examples:
        select * from pipes
    """
    pid = BigIntegerField(help_text="Process ID of the process to which the pipe belongs")  # {'index': True}
    name = TextField(help_text="Name of the pipe")
    instances = IntegerField(help_text="Number of instances of the named pipe")
    max_instances = IntegerField(help_text="The maximum number of instances creatable for this pipe")
    flags = TextField(help_text="The flags indicating whether this pipe connection is a server or client end, and if the pipe for sending messages or bytes")

    class Meta:
        table_name = "pipes"
