"""
OSQuery programs ORM
"""
from ...orm import BaseModel
from peewee import TextField


class Programs(BaseModel):
    """
    Represents products as they are installed by Windows Installer. A product generally correlates to one installation package on Windows. Some fields may be blank as Windows installation details are left to the discretion of the product author.
    Examples:
        select * from programs
        select name, install_location from programs where install_location not like 'C:\Program Files%';
    """
    name = TextField(help_text="Commonly used product name.")
    version = TextField(help_text="Product version information.")
    install_location = TextField(help_text="The installation location directory of the product.")
    install_source = TextField(help_text="The installation source of the product.")
    language = TextField(help_text="The language of the product.")
    publisher = TextField(help_text="Name of the product supplier.")
    uninstall_string = TextField(help_text="Path and filename of the uninstaller.")
    install_date = TextField(help_text="Date that this product was installed on the system. ")
    identifying_number = TextField(help_text="Product identification such as a serial number on software, or a die number on a hardware chip.")

    class Meta:
        table_name = "programs"
