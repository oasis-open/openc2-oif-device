"""
OSQuery hvci_status ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class HvciStatus(BaseModel):
    """
    Retrieve HVCI info of the machine.
    """
    version = TextField(help_text="The version number of the Device Guard build.")
    instance_identifier = TextField(help_text="The instance ID of Device Guard.")
    vbs_status = TextField(help_text="The status of the virtualization based security settings. Returns UNKNOWN if an error is encountered.")
    code_integrity_policy_enforcement_status = TextField(help_text="The status of the code integrity policy enforcement settings. Returns UNKNOWN if an error is encountered.")
    umci_policy_status = TextField(help_text="The status of the User Mode Code Integrity security settings. Returns UNKNOWN if an error is encountered.")

    class Meta:
        table_name = "hvci_status"
