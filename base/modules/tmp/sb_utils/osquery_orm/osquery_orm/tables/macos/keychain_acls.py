"""
OSQuery keychain_acls ORM
"""
from ...orm import BaseModel
from peewee import TextField


class KeychainAcls(BaseModel):
    """
    Applications that have ACL entries in the keychain.
    Examples:
        select label, description, authorizations, path, count(path) as c from keychain_acls where label != '' and path != '' group by label having c > 1;
    """
    keychain_path = TextField(help_text="The path of the keychain")
    authorizations = TextField(help_text="A space delimited set of authorization attributes")
    path = TextField(help_text="The path of the authorized application")
    description = TextField(help_text="The description included with the ACL entry")
    label = TextField(help_text="An optional label tag that may be included with the keychain entry")

    class Meta:
        table_name = "keychain_acls"
