"""
OSQuery video_info ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class VideoInfo(BaseModel):
    """
    Retrieve video card information of the machine.
    """
    color_depth = IntegerField(help_text="The amount of bits per pixel to represent color.")
    driver = TextField(help_text="The driver of the device.")
    driver_date = BigIntegerField(help_text="The date listed on the installed driver.")
    driver_version = TextField(help_text="The version of the installed driver.")
    manufacturer = TextField(help_text="The manufacturer of the gpu.")
    model = TextField(help_text="The model of the gpu.")
    series = TextField(help_text="The series of the gpu.")
    video_mode = TextField(help_text="The current resolution of the display.")

    class Meta:
        table_name = "video_info"
