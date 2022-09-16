"""
OSQuery docker_volume_labels ORM
"""
from ....orm import BaseModel
from peewee import TextField


class DockerVolumeLabels(BaseModel):
    """
    Docker volume labels.
    Examples:
        select * from docker_volume_labels
        select * from docker_volume_labels where name = 'btrfs'
    """
    name = TextField(help_text="Volume name")  # {'index': True}
    key = TextField(help_text="Label key")  # {'index': True}
    value = TextField(help_text="Optional label value")

    class Meta:
        table_name = "docker_volume_labels"
