"""
OSQuery ntdomains ORM
"""
from ...orm import BaseModel
from peewee import TextField


class Ntdomains(BaseModel):
    """
    Display basic NT domain information of a Windows machine.
    Examples:
        select * from ntdomains
    """
    name = TextField(help_text="The label by which the object is known.")
    client_site_name = TextField(help_text="The name of the site where the domain controller is configured.")
    dc_site_name = TextField(help_text="The name of the site where the domain controller is located.")
    dns_forest_name = TextField(help_text="The name of the root of the DNS tree.")
    domain_controller_address = TextField(help_text="The IP Address of the discovered domain controller..")
    domain_controller_name = TextField(help_text="The name of the discovered domain controller.")
    domain_name = TextField(help_text="The name of the domain.")
    status = TextField(help_text="The current status of the domain object.")

    class Meta:
        table_name = "ntdomains"
