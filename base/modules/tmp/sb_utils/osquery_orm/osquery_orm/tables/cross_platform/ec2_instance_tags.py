"""
OSQuery ec2_instance_tags ORM
"""
from ...orm import BaseModel
from peewee import TextField


class Ec2InstanceTags(BaseModel):
    """
    EC2 instance tag key value pairs.
    Examples:
        select * from ec2_instance_tags
    """
    instance_id = TextField(help_text="EC2 instance ID")
    key = TextField(help_text="Tag key")
    value = TextField(help_text="Tag value")

    class Meta:
        table_name = "ec2_instance_tags"
