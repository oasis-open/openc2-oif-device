"""
OSQuery windows_security_center ORM
"""
from ...orm import BaseModel
from peewee import TextField


class WindowsSecurityCenter(BaseModel):
    """
    The health status of Window Security features. Health values can be \"Good\", \"Poor\". \"Snoozed\", \"Not Monitored\", and \"Error\".
    Examples:
        select * from windows_security_center
    """
    firewall = TextField(help_text="The health of the monitored Firewall (see windows_security_products)")
    autoupdate = TextField(help_text="The health of the Windows Autoupdate feature")
    antivirus = TextField(help_text="The health of the monitored Antivirus solution (see windows_security_products)")
    antispyware = TextField(help_text="Deprecated (always \'Good\').")  # {'hidden': True}
    internet_settings = TextField(help_text="The health of the Internet Settings")
    windows_security_center_service = TextField(help_text="The health of the Windows Security Center Service")
    user_account_control = TextField(help_text="The health of the User Account Control (UAC) capability in Windows")

    class Meta:
        table_name = "windows_security_center"
