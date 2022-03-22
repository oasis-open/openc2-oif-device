"""
OSQuery file ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class File(BaseModel):
    """
    Interactive filesystem attributes and metadata.
    Examples:
        select * from file where path = '/etc/passwd'
        select * from file where directory = '/etc/'
        select * from file where path LIKE '/etc/%'
    """
    path = TextField(help_text="Absolute file path")  # {'required': True, 'index': True}
    directory = TextField(help_text="Directory of file(s)")  # {'required': True}
    filename = TextField(help_text="Name portion of file path")
    inode = BigIntegerField(help_text="Filesystem inode number")
    uid = BigIntegerField(help_text="Owning user ID")
    gid = BigIntegerField(help_text="Owning group ID")
    mode = TextField(help_text="Permission bits")
    device = BigIntegerField(help_text="Device ID (optional)")
    size = BigIntegerField(help_text="Size of file in bytes")
    block_size = IntegerField(help_text="Block size of filesystem")
    atime = BigIntegerField(help_text="Last access time")
    mtime = BigIntegerField(help_text="Last modification time")
    ctime = BigIntegerField(help_text="Last status change time")
    btime = BigIntegerField(help_text="(B)irth or (cr)eate time")
    hard_links = IntegerField(help_text="Number of hard links")
    symlink = IntegerField(help_text="1 if the path is a symlink, otherwise 0")
    type = TextField(help_text="File status")

    class Meta:
        table_name = "file"


# OS specific properties for Windows
class Windows_File(File):
    attributes = TextField(help_text="File attrib string. See: https://ss64.com/nt/attrib.html")
    volume_serial = TextField(help_text="Volume serial number")
    file_id = TextField(help_text="file ID")
    file_version = TextField(help_text="File version")
    product_version = TextField(help_text="File product version")

    class Meta:
        table_name = "file"


# OS specific properties for MacOS
class MacOS_File(File):
    bsd_flags = TextField(help_text="The BSD file flags (chflags). Possible values: NODUMP, UF_IMMUTABLE, UF_APPEND, OPAQUE, HIDDEN, ARCHIVED, SF_IMMUTABLE, SF_APPEND")

    class Meta:
        table_name = "file"


# OS specific properties for Linux
class Linux_File(File):
    pid_with_namespace = IntegerField(help_text="Pids that contain a namespace")  # {'additional': True, 'hidden': True}
    mount_namespace_id = TextField(help_text="Mount namespace id")  # {'hidden': True}

    class Meta:
        table_name = "file"
