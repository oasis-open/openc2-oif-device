"""
OSQuery apps ORM
"""
from ...orm import BaseModel
from peewee import DoubleField, TextField


class Apps(BaseModel):
    """
    OS X applications installed in known search paths (e.g., /Applications).
    """
    name = TextField(help_text="Name of the Name.app folder")
    path = TextField(help_text="Absolute and full Name.app path")  # {'index': True}
    bundle_executable = TextField(help_text="Info properties CFBundleExecutable label")
    bundle_identifier = TextField(help_text="Info properties CFBundleIdentifier label")
    bundle_name = TextField(help_text="Info properties CFBundleName label")
    bundle_short_version = TextField(help_text="Info properties CFBundleShortVersionString label")
    bundle_version = TextField(help_text="Info properties CFBundleVersion label")
    bundle_package_type = TextField(help_text="Info properties CFBundlePackageType label")
    environment = TextField(help_text="Application-set environment variables")
    element = TextField(help_text="Does the app identify as a background agent")
    compiler = TextField(help_text="Info properties DTCompiler label")
    development_region = TextField(help_text="Info properties CFBundleDevelopmentRegion label")
    display_name = TextField(help_text="Info properties CFBundleDisplayName label")
    info_string = TextField(help_text="Info properties CFBundleGetInfoString label")
    minimum_system_version = TextField(help_text="Minimum version of OS X required for the app to run")
    category = TextField(help_text="The UTI that categorizes the app for the App Store")
    applescript_enabled = TextField(help_text="Info properties NSAppleScriptEnabled label")
    copyright = TextField(help_text="Info properties NSHumanReadableCopyright label")
    last_opened_time = DoubleField(help_text="The time that the app was last used")

    class Meta:
        table_name = "apps"
