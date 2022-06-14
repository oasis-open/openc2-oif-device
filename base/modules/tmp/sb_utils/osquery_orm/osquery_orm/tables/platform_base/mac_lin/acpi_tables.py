"""
OSQuery acpi_tables ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class AcpiTables(BaseModel):
    """
    Firmware ACPI functional table common metadata and content.
    """
    name = TextField(help_text="ACPI table name")
    size = IntegerField(help_text="Size of compiled table data")
    md5 = TextField(help_text="MD5 hash of table content")

    class Meta:
        table_name = "acpi_tables"
