"""
OSQuery chrome_extensions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, ForeignKeyField, IntegerField, TextField
from .users import Users


class ChromeExtensions(BaseModel):
    """
    Chrome-based browser extensions.
    Examples:
        select * from users join chrome_extensions using (uid)
    """
    browser_type = TextField(help_text="The browser type (Valid values: chrome, chromium, opera, yandex, brave, edge, edge_beta)")
    uid = BigIntegerField(help_text="The local user that owns the extension")  # {'index': True}
    name = TextField(help_text="Extension display name")
    profile = TextField(help_text="The name of the Chrome profile that contains this extension")
    profile_path = TextField(help_text="The profile path")
    referenced_identifier = TextField(help_text="Extension identifier, as specified by the preferences file. Empty if the extension is not in the profile.")
    identifier = TextField(help_text="Extension identifier, computed from its manifest. Empty in case of error.")
    version = TextField(help_text="Extension-supplied version")
    description = TextField(help_text="Extension-optional description")
    default_locale = TextField(help_text="Default locale supported by extension")  # {'aliases': ['locale']}
    current_locale = TextField(help_text="Current locale supported by extension")
    update_url = TextField(help_text="Extension-supplied update URI")
    author = TextField(help_text="Optional extension author")
    persistent = IntegerField(help_text="1 If extension is persistent across all tabs else 0")
    path = TextField(help_text="Path to extension folder")
    permissions = TextField(help_text="The permissions required by the extension")
    permissions_json = TextField(help_text="The JSON-encoded permissions required by the extension")  # {'hidden': True}
    optional_permissions = TextField(help_text="The permissions optionally required by the extensions")
    optional_permissions_json = TextField(help_text="The JSON-encoded permissions optionally required by the extensions")  # {'hidden': True}
    manifest_hash = TextField(help_text="The SHA256 hash of the manifest.json file")
    referenced = BigIntegerField(help_text="1 if this extension is referenced by the Preferences file of the profile")
    from_webstore = TextField(help_text="True if this extension was installed from the web store")
    state = TextField(help_text="1 if this extension is enabled")
    install_time = TextField(help_text="Extension install time, in its original Webkit format")
    install_timestamp = BigIntegerField(help_text="Extension install time, converted to unix time")
    manifest_json = TextField(help_text="The manifest file of the extension")  # {'hidden': True}
    key = TextField(help_text="The extension key, from the manifest file")  # {'hidden': True}
    chrome_extensions = ForeignKeyField(Users, backref='uid')

    class Meta:
        table_name = "chrome_extensions"
