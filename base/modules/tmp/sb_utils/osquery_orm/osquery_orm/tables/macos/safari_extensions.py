"""
OSQuery safari_extensions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, TextField
from ..cross_platform import MacOS_Users


class SafariExtensions(BaseModel):
    """
    Safari browser extension details for all users.
    Examples:
        select count(*) from users JOIN safari_extensions using (uid)
    """
    uid = BigIntegerField(help_text="The local user that owns the extension")  # {'index': True}
    name = TextField(help_text="Extension display name")
    identifier = TextField(help_text="Extension identifier")
    version = TextField(help_text="Extension long version")
    sdk = TextField(help_text="Bundle SDK used to compile extension")
    update_url = TextField(help_text="Extension-supplied update URI")
    author = TextField(help_text="Optional extension author")
    developer_id = TextField(help_text="Optional developer identifier")
    description = TextField(help_text="Optional extension description text")
    path = TextField(help_text="Path to extension XAR bundle")
    safari_extensions = ForeignKeyField(MacOS_Users, backref='uid')

    class Meta:
        table_name = "safari_extensions"
