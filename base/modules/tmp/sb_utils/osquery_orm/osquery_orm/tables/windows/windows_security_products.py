"""
OSQuery windows_security_products ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class WindowsSecurityProducts(BaseModel):
    """
    Enumeration of registered Windows security products.
    Examples:
        select * from windows_security_products
    """
    type = TextField(help_text="Type of security product")
    name = TextField(help_text="Name of product")
    state = TextField(help_text="State of protection")
    state_timestamp = TextField(help_text="Timestamp for the product state")
    remediation_path = TextField(help_text="Remediation path")
    signatures_up_to_date = IntegerField(help_text="1 if product signatures are up to date, else 0")

    class Meta:
        table_name = "windows_security_products"
