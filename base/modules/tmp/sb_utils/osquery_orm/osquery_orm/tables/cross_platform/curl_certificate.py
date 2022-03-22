"""
OSQuery curl_certificate ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class CurlCertificate(BaseModel):
    """
    Inspect TLS certificates by connecting to input hostnames.
    Examples:
        select * from curl_certificate where hostname = 'osquery.io'select * from curl_certificate where hostname = 'osquery.io' and dump_certificate = 1
    """
    hostname = TextField(help_text="Hostname (domain[:port]) to CURL")  # {'required': True}
    common_name = TextField(help_text="Common name of company issued to")
    organization = TextField(help_text="Organization issued to")
    organization_unit = TextField(help_text="Organization unit issued to")
    serial_number = TextField(help_text="Certificate serial number")
    issuer_common_name = TextField(help_text="Issuer common name")
    issuer_organization = TextField(help_text="Issuer organization")
    issuer_organization_unit = TextField(help_text="Issuer organization unit")
    valid_from = TextField(help_text="Period of validity start date")
    valid_to = TextField(help_text="Period of validity end date")
    sha256_fingerprint = TextField(help_text="SHA-256 fingerprint")
    sha1_fingerprint = TextField(help_text="SHA1 fingerprint")
    version = IntegerField(help_text="Version Number")
    signature_algorithm = TextField(help_text="Signature Algorithm")
    signature = TextField(help_text="Signature")
    subject_key_identifier = TextField(help_text="Subject Key Identifier")
    authority_key_identifier = TextField(help_text="Authority Key Identifier")
    key_usage = TextField(help_text="Usage of key in certificate")
    extended_key_usage = TextField(help_text="Extended usage of key in certificate")
    policies = TextField(help_text="Certificate Policies")
    subject_alternative_names = TextField(help_text="Subject Alternative Name")
    issuer_alternative_names = TextField(help_text="Issuer Alternative Name")
    info_access = TextField(help_text="Authority Information Access")
    subject_info_access = TextField(help_text="Subject Information Access")
    policy_mappings = TextField(help_text="Policy Mappings")
    has_expired = IntegerField(help_text="1 if the certificate has expired, 0 otherwise")
    basic_constraint = TextField(help_text="Basic Constraints")
    name_constraints = TextField(help_text="Name Constraints")
    policy_constraints = TextField(help_text="Policy Constraints")
    dump_certificate = IntegerField(help_text="Set this value to \'1\' to dump certificate")  # {'additional': True, 'hidden': True}
    timeout = IntegerField(help_text="Set this value to the timeout in seconds to complete the TLS handshake (default 4s, use 0 for no timeout)")  # {'additional': True, 'hidden': True}
    pem = TextField(help_text="Certificate PEM format")

    class Meta:
        table_name = "curl_certificate"
