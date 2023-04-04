"""
OSQuery package_install_history ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class PackageInstallHistory(BaseModel):
    """
    OS X package install history.
    """
    package_id = TextField(help_text="Label packageIdentifiers")
    time = IntegerField(help_text="Label date as UNIX timestamp")
    name = TextField(help_text="Package display name")
    version = TextField(help_text="Package display version")
    source = TextField(help_text="Install source: usually the installer process name")
    content_type = TextField(help_text="Package content_type (optional)")

    class Meta:
        table_name = "package_install_history"
