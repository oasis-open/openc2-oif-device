"""
OSQuery account_policy_data ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, DoubleField, ForeignKeyField
from ..cross_platform import MacOS_Users


class AccountPolicyData(BaseModel):
    """
    Additional OS X user account data from the AccountPolicy section of OpenDirectory.
    Examples:
        select * from users join account_policy_data using (uid)
    """
    uid = BigIntegerField(help_text="User ID")
    creation_time = DoubleField(help_text="When the account was first created")
    failed_login_count = BigIntegerField(help_text="The number of failed login attempts using an incorrect password. Count resets after a correct password is entered.")
    failed_login_timestamp = DoubleField(help_text="The time of the last failed login attempt. Resets after a correct password is entered")
    password_last_set_time = DoubleField(help_text="The time the password was last changed")
    account_policy_data = ForeignKeyField(MacOS_Users, backref='uid')

    class Meta:
        table_name = "account_policy_data"
