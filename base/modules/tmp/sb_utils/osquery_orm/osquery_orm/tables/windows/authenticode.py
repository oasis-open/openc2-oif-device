"""
OSQuery authenticode ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Authenticode(BaseModel):
    """
    File (executable, bundle, installer, disk) code signing status.
    Examples:
        SELECT * FROM authenticode WHERE path = 'C:\Windows\notepad.exe'
        SELECT process.pid, process.path, signature.result FROM processes as process LEFT JOIN authenticode AS signature ON process.path = signature.path;
    """
    path = TextField(help_text="Must provide a path or directory")  # {'required': True}
    original_program_name = TextField(help_text="The original program name that the publisher has signed")
    serial_number = TextField(help_text="The certificate serial number")
    issuer_name = TextField(help_text="The certificate issuer name")
    subject_name = TextField(help_text="The certificate subject name")
    result = TextField(help_text="The signature check result")

    class Meta:
        table_name = "authenticode"
