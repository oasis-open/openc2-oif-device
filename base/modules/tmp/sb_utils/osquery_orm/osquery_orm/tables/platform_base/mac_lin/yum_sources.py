"""
OSQuery yum_sources ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class YumSources(BaseModel):
    """
    Current list of Yum repositories or software channels.
    """
    name = TextField(help_text="Repository name")
    baseurl = TextField(help_text="Repository base URL")
    enabled = TextField(help_text="Whether the repository is used")
    gpgcheck = TextField(help_text="Whether packages are GPG checked")
    gpgkey = TextField(help_text="URL to GPG key")

    class Meta:
        table_name = "yum_sources"


# OS specific properties for Linux
class Linux_YumSources(YumSources):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "yum_sources"
