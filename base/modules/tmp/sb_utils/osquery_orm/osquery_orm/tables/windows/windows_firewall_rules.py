"""
OSQuery windows_firewall_rules ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class WindowsFirewallRules(BaseModel):
    """
    Provides the list of Windows firewall rules.
    Examples:
        select * from windows_firewall_rules
    """
    name = TextField(help_text="Friendly name of the rule")
    app_name = TextField(help_text="Friendly name of the application to which the rule applies")
    action = TextField(help_text="Action for the rule or default setting")
    enabled = IntegerField(help_text="1 if the rule is enabled")
    grouping = TextField(help_text="Group to which an individual rule belongs")
    direction = TextField(help_text="Direction of traffic for which the rule applies")
    protocol = TextField(help_text="IP protocol of the rule")
    local_addresses = TextField(help_text="Local addresses for the rule")
    remote_addresses = TextField(help_text="Remote addresses for the rule")
    local_ports = TextField(help_text="Local ports for the rule")
    remote_ports = TextField(help_text="Remote ports for the rule")
    icmp_types_codes = TextField(help_text="ICMP types and codes for the rule")
    profile_domain = IntegerField(help_text="1 if the rule profile type is domain")
    profile_private = IntegerField(help_text="1 if the rule profile type is private")
    profile_public = IntegerField(help_text="1 if the rule profile type is public")
    service_name = TextField(help_text="Service name property of the application")

    class Meta:
        table_name = "windows_firewall_rules"
