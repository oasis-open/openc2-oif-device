"""
OSQuery ssh_configs ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, TextField
from .users import Users


class SshConfigs(BaseModel):
    """
    A table of parsed ssh_configs.
    Examples:
        select * from users join ssh_configs using (uid)
    """
    uid = BigIntegerField(help_text="The local owner of the ssh_config file")  # {'additional': True}
    block = TextField(help_text="The host or match block")
    option = TextField(help_text="The option and value")
    ssh_config_file = TextField(help_text="Path to the ssh_config file")
    ssh_configs = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "ssh_configs"
