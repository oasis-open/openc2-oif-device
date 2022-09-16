"""
OSQuery apparmor_profiles ORM
"""
from ...orm import BaseModel
from peewee import TextField


class ApparmorProfiles(BaseModel):
    """
    Track active AppArmor profiles.
    Examples:
        SELECT * FROM apparmor_profiles WHERE mode = 'complain'
    """
    path = TextField(help_text="Unique, aa-status compatible, policy identifier.")  # {'index': True}
    name = TextField(help_text="Policy name.")
    attach = TextField(help_text="Which executable(s) a profile will attach to.")
    mode = TextField(help_text="How the policy is applied.")
    sha1 = TextField(help_text="A unique hash that identifies this policy.")

    class Meta:
        table_name = "apparmor_profiles"
