"""
OSQuery user_ssh_keys ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from .users import Users


class UserSshKeys(BaseModel):
    """
    Returns the private keys in the users ~/.ssh directory and whether or not they are encrypted.
    Examples:
        select * from users join user_ssh_keys using (uid) where encrypted = 0
    """
    uid = BigIntegerField(help_text="The local user that owns the key file")  # {'additional': True}
    path = TextField(help_text="Path to key file")  # {'index': True}
    encrypted = IntegerField(help_text="1 if key is encrypted, 0 otherwise")
    key_type = TextField(help_text="The type of the private key. One of [rsa, dsa, dh, ec, hmac, cmac], or the empty string.")
    user_ssh_keys = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "user_ssh_keys"


# OS specific properties for Linux
class Linux_UserSshKeys(UserSshKeys):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "user_ssh_keys"
