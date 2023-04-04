"""
OSQuery wifi_status ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class WifiStatus(BaseModel):
    """
    OS X current WiFi status.
    """
    interface = TextField(help_text="Name of the interface")
    ssid = TextField(help_text="SSID octets of the network")
    bssid = TextField(help_text="The current basic service set identifier")
    network_name = TextField(help_text="Name of the network")
    country_code = TextField(help_text="The country code (ISO/IEC 3166-1:1997) for the network")
    security_type = TextField(help_text="Type of security on this network")
    rssi = IntegerField(help_text="The current received signal strength indication (dbm)")
    noise = IntegerField(help_text="The current noise measurement (dBm)")
    channel = IntegerField(help_text="Channel number")
    channel_width = IntegerField(help_text="Channel width")
    channel_band = IntegerField(help_text="Channel band")
    transmit_rate = TextField(help_text="The current transmit rate")
    mode = TextField(help_text="The current operating mode for the Wi-Fi interface")

    class Meta:
        table_name = "wifi_status"
