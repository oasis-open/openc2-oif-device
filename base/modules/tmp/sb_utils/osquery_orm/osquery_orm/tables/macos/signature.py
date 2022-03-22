"""
OSQuery signature ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Signature(BaseModel):
    """
    File (executable, bundle, installer, disk) code signing status.
    Examples:
        SELECT * FROM signature WHERE path = '/bin/ls'
        SELECT * FROM signature WHERE path = '/Applications/Xcode.app' AND hash_resources=0
        SELECT * FROM (SELECT path, MIN(signed) AS all_signed, MIN(CASE WHEN authority = 'Software Signing' AND signed = 1 THEN 1 ELSE 0 END) AS all_signed_by_apple FROM signature WHERE path LIKE '/bin/%' GROUP BY path);
    """
    path = TextField(help_text="Must provide a path or directory")  # {'index': True, 'required': True}
    hash_resources = IntegerField(help_text="Set to 1 to also hash resources, or 0 otherwise. Default is 1")  # {'additional': True}
    arch = TextField(help_text="If applicable, the arch of the signed code")
    signed = IntegerField(help_text="1 If the file is signed else 0")
    identifier = TextField(help_text="The signing identifier sealed into the signature")
    cdhash = TextField(help_text="Hash of the application Code Directory")
    team_identifier = TextField(help_text="The team signing identifier sealed into the signature")
    authority = TextField(help_text="Certificate Common Name")

    class Meta:
        table_name = "signature"
