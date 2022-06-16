"""
OSQuery ntfs_acl_permissions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class NtfsAclPermissions(BaseModel):
    """
    Retrieve NTFS ACL permission information for files and directories.
    """
    path = TextField(help_text="Path to the file or directory.")  # {'required': True, 'index': True}
    type = TextField(help_text="Type of access mode for the access control entry.")
    principal = TextField(help_text="User or group to which the ACE applies.")
    access = TextField(help_text="Specific permissions that indicate the rights described by the ACE.")
    inherited_from = TextField(help_text="The inheritance policy of the ACE.")

    class Meta:
        table_name = "ntfs_acl_permissions"
