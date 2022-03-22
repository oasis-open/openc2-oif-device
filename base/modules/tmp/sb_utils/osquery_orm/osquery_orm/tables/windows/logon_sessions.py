"""
OSQuery logon_sessions ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class LogonSessions(BaseModel):
    """
    Windows Logon Session.
    Examples:
        select * from logon_sessions;
    """
    logon_id = IntegerField(help_text="A locally unique identifier (LUID) that identifies a logon session.")
    user = TextField(help_text="The account name of the security principal that owns the logon session.")
    logon_domain = TextField(help_text="The name of the domain used to authenticate the owner of the logon session.")
    authentication_package = TextField(help_text="The authentication package used to authenticate the owner of the logon session.")
    logon_type = TextField(help_text="The logon method.")
    session_id = IntegerField(help_text="The Terminal Services session identifier.")
    logon_sid = TextField(help_text="The user\'s security identifier (SID).")
    logon_time = BigIntegerField(help_text="The time the session owner logged on.")
    logon_server = TextField(help_text="The name of the server used to authenticate the owner of the logon session.")
    dns_domain_name = TextField(help_text="The DNS name for the owner of the logon session.")
    upn = TextField(help_text="The user principal name (UPN) for the owner of the logon session.")
    logon_script = TextField(help_text="The script used for logging on.")
    profile_path = TextField(help_text="The home directory for the logon session.")
    home_directory = TextField(help_text="The home directory for the logon session.")
    home_directory_drive = TextField(help_text="The drive location of the home directory of the logon session.")

    class Meta:
        table_name = "logon_sessions"
