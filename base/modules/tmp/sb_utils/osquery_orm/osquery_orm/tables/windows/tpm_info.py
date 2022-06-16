"""
OSQuery tpm_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class TpmInfo(BaseModel):
    """
    A table that lists the TPM related information.
    Examples:
        select * from tpm_info
    """
    activated = IntegerField(help_text="TPM is activated")
    enabled = IntegerField(help_text="TPM is enabled")
    owned = IntegerField(help_text="TPM is ownned")
    manufacturer_version = TextField(help_text="TPM version")
    manufacturer_id = IntegerField(help_text="TPM manufacturers ID")
    manufacturer_name = TextField(help_text="TPM manufacturers name")
    product_name = TextField(help_text="Product name of the TPM")
    physical_presence_version = TextField(help_text="Version of the Physical Presence Interface")
    spec_version = TextField(help_text="Trusted Computing Group specification that the TPM supports")

    class Meta:
        table_name = "tpm_info"
