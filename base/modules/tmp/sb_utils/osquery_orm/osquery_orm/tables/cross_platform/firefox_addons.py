"""
OSQuery firefox_addons ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from .users import Users


class FirefoxAddons(BaseModel):
    """
    Firefox browser extensions, webapps, and addons.
    Examples:
        select * from users join firefox_addons using (uid)
    """
    uid = BigIntegerField(help_text="The local user that owns the addon")  # {'additional': True}
    name = TextField(help_text="Addon display name")
    identifier = TextField(help_text="Addon identifier")  # {'index': True}
    creator = TextField(help_text="Addon-supported creator string")
    type = TextField(help_text="Extension, addon, webapp")
    version = TextField(help_text="Addon-supplied version string")
    description = TextField(help_text="Addon-supplied description string")
    source_url = TextField(help_text="URL that installed the addon")
    visible = IntegerField(help_text="1 If the addon is shown in browser else 0")
    active = IntegerField(help_text="1 If the addon is active else 0")
    disabled = IntegerField(help_text="1 If the addon is application-disabled else 0")
    autoupdate = IntegerField(help_text="1 If the addon applies background updates else 0")
    native = IntegerField(help_text="1 If the addon includes binary components else 0")
    location = TextField(help_text="Global, profile location")
    path = TextField(help_text="Path to plugin bundle")
    firefox_addons = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "firefox_addons"
