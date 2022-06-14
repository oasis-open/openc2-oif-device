"""
OSQuery hash ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Hash(BaseModel):
    """
    Filesystem hash data.
    Examples:
        select * from hash where path = '/etc/passwd'
        select * from hash where directory = '/etc/'
    """
    path = TextField(help_text="Must provide a path or directory")  # {'index': True, 'required': True}
    directory = TextField(help_text="Must provide a path or directory")  # {'required': True}
    md5 = TextField(help_text="MD5 hash of provided filesystem data")
    sha1 = TextField(help_text="SHA1 hash of provided filesystem data")
    sha256 = TextField(help_text="SHA256 hash of provided filesystem data")

    class Meta:
        table_name = "hash"


# OS specific properties for Posix
class Posix_Hash(Hash):
    ssdeep = TextField(help_text="ssdeep hash of provided filesystem data")

    class Meta:
        table_name = "hash"


# OS specific properties for Linux
class Linux_Hash(Hash):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "hash"
