"""
OSQuery lxd_images ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class LxdImages(BaseModel):
    """
    LXD images information.
    Examples:
        select * from lxd_images
        select * from lxd_images where id = '0931b693c8'
        select * from lxd_images where id = '0931b693c877ef357b9e17b3195ae952a2450873923ffd2b34b60836ea730cfa'
    """
    id = TextField(help_text="Image ID")  # {'index': True}
    architecture = TextField(help_text="Target architecture for the image")
    os = TextField(help_text="OS on which image is based")
    release = TextField(help_text="OS release version on which the image is based")
    description = TextField(help_text="Image description")
    aliases = TextField(help_text="Comma-separated list of image aliases")
    filename = TextField(help_text="Filename of the image file")
    size = BigIntegerField(help_text="Size of image in bytes")
    auto_update = IntegerField(help_text="Whether the image auto-updates (1) or not (0)")
    cached = IntegerField(help_text="Whether image is cached (1) or not (0)")
    public = IntegerField(help_text="Whether image is public (1) or not (0)")
    created_at = TextField(help_text="ISO time of image creation")
    expires_at = TextField(help_text="ISO time of image expiration")
    uploaded_at = TextField(help_text="ISO time of image upload")
    last_used_at = TextField(help_text="ISO time for the most recent use of this image in terms of container spawn")
    update_source_server = TextField(help_text="Server for image update")
    update_source_protocol = TextField(help_text="Protocol used for image information update and image import from source server")
    update_source_certificate = TextField(help_text="Certificate for update source server")
    update_source_alias = TextField(help_text="Alias of image at update source server")

    class Meta:
        table_name = "lxd_images"
