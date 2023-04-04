"""
OSQuery docker_image_labels ORM
"""
from ....orm import BaseModel
from peewee import TextField


class DockerImageLabels(BaseModel):
    """
    Docker image labels.
    Examples:
        select * from docker_image_labels
        select * from docker_image_labels where id = '1234567890abcdef'
        select * from docker_image_labels where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
    """
    id = TextField(help_text="Image ID")  # {'index': True}
    key = TextField(help_text="Label key")
    value = TextField(help_text="Optional label value")

    class Meta:
        table_name = "docker_image_labels"
