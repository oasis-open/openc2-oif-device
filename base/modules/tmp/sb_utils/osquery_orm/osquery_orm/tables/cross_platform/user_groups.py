"""
OSQuery user_groups ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField


class UserGroups(BaseModel):
    """
    Local system user group relationships.
    """
    uid = BigIntegerField(help_text="User ID")  # {'index': True}
    gid = BigIntegerField(help_text="Group ID")  # {'index': True}

    class Meta:
        table_name = "user_groups"
