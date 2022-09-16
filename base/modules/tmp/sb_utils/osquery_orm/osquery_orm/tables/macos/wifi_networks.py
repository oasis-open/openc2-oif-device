"""
OSQuery wifi_networks ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class WifiNetworks(BaseModel):
    """
    OS X known/remembered Wi-Fi networks list.
    """
    ssid = TextField(help_text="SSID octets of the network")
    network_name = TextField(help_text="Name of the network")
    security_type = TextField(help_text="Type of security on this network")
    last_connected = IntegerField(help_text="Last time this netword was connected to as a unix_time")
    passpoint = IntegerField(help_text="1 if Passpoint is supported, 0 otherwise")
    possibly_hidden = IntegerField(help_text="1 if network is possibly a hidden network, 0 otherwise")
    roaming = IntegerField(help_text="1 if roaming is supported, 0 otherwise")
    roaming_profile = TextField(help_text="Describe the roaming profile, usually one of Single, Dual  or Multi")
    captive_portal = IntegerField(help_text="1 if this network has a captive portal, 0 otherwise")
    auto_login = IntegerField(help_text="1 if auto login is enabled, 0 otherwise")
    temporarily_disabled = IntegerField(help_text="1 if this network is temporarily disabled, 0 otherwise")
    disabled = IntegerField(help_text="1 if this network is disabled, 0 otherwise")

    class Meta:
        table_name = "wifi_networks"
