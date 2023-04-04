"""
OSQuery docker_images ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, TextField


class DockerImages(BaseModel):
    """
    Docker images information.
    Examples:
        select * from docker_images
        select * from docker_images where id = '6a2f32de169d'
        select * from docker_images where id = '6a2f32de169d14e6f8a84538eaa28f2629872d7d4f580a303b296c60db36fbd7'
    """
    id = TextField(help_text="Image ID")
    created = BigIntegerField(help_text="Time of creation as UNIX time")
    size_bytes = BigIntegerField(help_text="Size of image in bytes")
    tags = TextField(help_text="Comma-separated list of repository tags")

    class Meta:
        table_name = "docker_images"
