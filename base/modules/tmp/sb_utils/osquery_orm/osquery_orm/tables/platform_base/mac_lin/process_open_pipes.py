"""
OSQuery process_open_pipes ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class ProcessOpenPipes(BaseModel):
    """
    Pipes and partner processes for each process.
    Examples:
        select * from process_open_pipes
    """
    pid = BigIntegerField(help_text="Process ID")
    fd = BigIntegerField(help_text="File descriptor")
    mode = TextField(help_text="Pipe open mode (r/w)")
    inode = BigIntegerField(help_text="Pipe inode number")
    type = TextField(help_text="Pipe Type: named vs unnamed/anonymous")
    partner_pid = BigIntegerField(help_text="Process ID of partner process sharing a particular pipe")
    partner_fd = BigIntegerField(help_text="File descriptor of shared pipe at partner\'s end")
    partner_mode = TextField(help_text="Mode of shared pipe at partner\'s end")

    class Meta:
        table_name = "process_open_pipes"
