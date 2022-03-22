"""
OSQuery managed_policies ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class ManagedPolicies(BaseModel):
    """
    The managed configuration policies from AD, MDM, MCX, etc.
    """
    domain = TextField(help_text="System or manager-chosen domain key")
    uuid = TextField(help_text="Optional UUID assigned to policy set")
    name = TextField(help_text="Policy key name")
    value = TextField(help_text="Policy value")
    username = TextField(help_text="Policy applies only this user")
    manual = IntegerField(help_text="1 if policy was loaded manually, otherwise 0")

    class Meta:
        table_name = "managed_policies"
