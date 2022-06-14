"""
OSQuery docker_image_history ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, TextField


class DockerImageHistory(BaseModel):
    """
    Docker image history information.
    Examples:
        select * from docker_image_history
        select * from docker_image_history where id = '6a2f32de169d'
        select * from docker_image_history where id = '6a2f32de169d14e6f8a84538eaa28f2629872d7d4f580a303b296c60db36fbd7'
    """
    id = TextField(help_text="Image ID")  # {'index': True}
    created = BigIntegerField(help_text="Time of creation as UNIX time")
    size = BigIntegerField(help_text="Size of instruction in bytes")
    created_by = TextField(help_text="Created by instruction")
    tags = TextField(help_text="Comma-separated list of tags")
    comment = TextField(help_text="Instruction comment")

    class Meta:
        table_name = "docker_image_history"
