"""
OSQuery browser_plugins ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from ..cross_platform import MacOS_Users


class BrowserPlugins(BaseModel):
    """
    All C/NPAPI browser plugin details for all users.
    Examples:
        select * from users join browser_plugins using (uid)
    """
    uid = BigIntegerField(help_text="The local user that owns the plugin")  # {'index': True}
    name = TextField(help_text="Plugin display name")
    identifier = TextField(help_text="Plugin identifier")
    version = TextField(help_text="Plugin short version")
    sdk = TextField(help_text="Build SDK used to compile plugin")
    description = TextField(help_text="Plugin description text")
    development_region = TextField(help_text="Plugin language-localization")
    native = IntegerField(help_text="Plugin requires native execution")
    path = TextField(help_text="Path to plugin bundle")  # {'index': True}
    disabled = IntegerField(help_text="Is the plugin disabled. 1 = Disabled")
    browser_plugins = ForeignKeyField(MacOS_Users, backref='uid')

    class Meta:
        table_name = "browser_plugins"
