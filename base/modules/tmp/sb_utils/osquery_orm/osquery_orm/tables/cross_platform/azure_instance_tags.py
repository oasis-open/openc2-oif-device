"""
OSQuery azure_instance_tags ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class AzureInstanceTags(BaseModel):
    """
    Azure instance tags.
    Examples:
        select * from ec2_instance_tags
    """
    vm_id = TextField(help_text="Unique identifier for the VM")
    key = TextField(help_text="The tag key")
    value = TextField(help_text="The tag value")

    class Meta:
        table_name = "azure_instance_tags"
