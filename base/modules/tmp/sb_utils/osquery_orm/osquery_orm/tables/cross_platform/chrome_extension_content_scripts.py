"""
OSQuery chrome_extension_content_scripts ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, TextField
from .users import Users


class ChromeExtensionContentScripts(BaseModel):
    """
    Chrome browser extension content scripts.
    Examples:
        SELECT chrome_extension_content_scripts.* FROM users JOIN chrome_extension_content_scripts USING (uid) GROUP BY identifier, match
    """
    browser_type = TextField(help_text="The browser type (Valid values: chrome, chromium, opera, yandex, brave)")
    uid = BigIntegerField(help_text="The local user that owns the extension")  # {'index': True}
    identifier = TextField(help_text="Extension identifier")
    version = TextField(help_text="Extension-supplied version")
    script = TextField(help_text="The content script used by the extension")
    match = TextField(help_text="The pattern that the script is matched against")
    profile_path = TextField(help_text="The profile path")
    path = TextField(help_text="Path to extension folder")
    referenced = BigIntegerField(help_text="1 if this extension is referenced by the Preferences file of the profile")
    chrome_extension_content_scripts = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "chrome_extension_content_scripts"
