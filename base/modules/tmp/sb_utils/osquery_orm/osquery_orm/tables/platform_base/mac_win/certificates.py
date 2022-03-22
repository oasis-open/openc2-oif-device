"""
OSQuery certificates ORM
"""
from osquery_orm.orm import BaseModel
from peewee import DateTimeField, IntegerField, TextField


class Certificates(BaseModel):
    """
    Certificate Authorities installed in Keychains/ca-bundles.
    """
    common_name = TextField(help_text="Certificate CommonName")
    subject = TextField(help_text="Certificate distinguished name")
    issuer = TextField(help_text="Certificate issuer distinguished name")
    ca = IntegerField(help_text="1 if CA: true (certificate is an authority) else 0")
    self_signed = IntegerField(help_text="1 if self-signed, else 0")
    not_valid_before = DateTimeField(help_text="Lower bound of valid date")
    not_valid_after = DateTimeField(help_text="Certificate expiration data")
    signing_algorithm = TextField(help_text="Signing algorithm used")
    key_algorithm = TextField(help_text="Key algorithm used")
    key_strength = TextField(help_text="Key size used for RSA/DSA, or curve name")
    key_usage = TextField(help_text="Certificate key usage and extended key usage")
    subject_key_id = TextField(help_text="SKID an optionally included SHA1")
    authority_key_id = TextField(help_text="AKID an optionally included SHA1")
    sha1 = TextField(help_text="SHA1 hash of the raw certificate contents")
    path = TextField(help_text="Path to Keychain or PEM bundle")  # {'additional': True}
    serial = TextField(help_text="Certificate serial number")

    class Meta:
        table_name = "certificates"


# OS specific properties for Windows
class Windows_Certificates(Certificates):
    sid = TextField(help_text="SID")
    store_location = TextField(help_text="Certificate system store location")
    store = TextField(help_text="Certificate system store")
    username = TextField(help_text="Username")
    store_id = TextField(help_text="Exists for service/user stores. Contains raw store id provided by WinAPI.")

    class Meta:
        table_name = "certificates"
