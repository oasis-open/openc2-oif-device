"""
OSQuery windows_optional_features ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class WindowsOptionalFeatures(BaseModel):
    """
    Lists names and installation states of windows features. Maps to Win32_OptionalFeature WMI class.
    Examples:
        select * from windows_optional_features
        select * from windows_optional_features where name = 'SMB1Protocol' AND state = 1
    """
    name = TextField(help_text="Name of the feature")
    caption = TextField(help_text="Caption of feature in settings UI")
    state = IntegerField(help_text="Installation state value. 1 == Enabled, 2 == Disabled, 3 == Absent")
    statename = TextField(help_text="Installation state name. \'Enabled\',\'Disabled\',\'Absent\'")

    class Meta:
        table_name = "windows_optional_features"
