"""
OSQuery azure_instance_metadata ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class AzureInstanceMetadata(BaseModel):
    """
    Azure instance metadata.
    Examples:
        select * from ec2_instance_metadata
    """
    location = TextField(help_text="Azure Region the VM is running in")
    name = TextField(help_text="Name of the VM")
    offer = TextField(help_text="Offer information for the VM image (Azure image gallery VMs only)")
    publisher = TextField(help_text="Publisher of the VM image")
    sku = TextField(help_text="SKU for the VM image")
    version = TextField(help_text="Version of the VM image")
    os_type = TextField(help_text="Linux or Windows")
    platform_update_domain = TextField(help_text="Update domain the VM is running in")
    platform_fault_domain = TextField(help_text="Fault domain the VM is running in")
    vm_id = TextField(help_text="Unique identifier for the VM")  # {'index': True}
    vm_size = TextField(help_text="VM size")
    subscription_id = TextField(help_text="Azure subscription for the VM")
    resource_group_name = TextField(help_text="Resource group for the VM")
    placement_group_id = TextField(help_text="Placement group for the VM scale set")
    vm_scale_set_name = TextField(help_text="VM scale set name")
    zone = TextField(help_text="Availability zone of the VM")

    class Meta:
        table_name = "azure_instance_metadata"
