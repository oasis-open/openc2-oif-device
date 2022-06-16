"""
OSQuery lxd_certificates ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class LxdCertificates(BaseModel):
    """
    LXD certificates information.
    Examples:
        select * from lxd_certificates
    """
    name = TextField(help_text="Name of the certificate")
    type = TextField(help_text="Type of the certificate")
    fingerprint = TextField(help_text="SHA256 hash of the certificate")
    certificate = TextField(help_text="Certificate content")

    class Meta:
        table_name = "lxd_certificates"
