"""
OSQuery sharing_preferences ORM
"""
from ...orm import BaseModel
from peewee import IntegerField


class SharingPreferences(BaseModel):
    """
    OS X Sharing preferences.
    """
    screen_sharing = IntegerField(help_text="1 If screen sharing is enabled else 0")
    file_sharing = IntegerField(help_text="1 If file sharing is enabled else 0")
    printer_sharing = IntegerField(help_text="1 If printer sharing is enabled else 0")
    remote_login = IntegerField(help_text="1 If remote login is enabled else 0")
    remote_management = IntegerField(help_text="1 If remote management is enabled else 0")
    remote_apple_events = IntegerField(help_text="1 If remote apple events are enabled else 0")
    internet_sharing = IntegerField(help_text="1 If internet sharing is enabled else 0")
    bluetooth_sharing = IntegerField(help_text="1 If bluetooth sharing is enabled for any user else 0")
    disc_sharing = IntegerField(help_text="1 If CD or DVD sharing is enabled else 0")
    content_caching = IntegerField(help_text="1 If content caching is enabled else 0")

    class Meta:
        table_name = "sharing_preferences"
