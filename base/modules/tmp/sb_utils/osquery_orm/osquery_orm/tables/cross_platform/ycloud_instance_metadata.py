"""
OSQuery ycloud_instance_metadata ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class YcloudInstanceMetadata(BaseModel):
    """
    Yandex.Cloud instance metadata.
    Examples:
        select * from ycloud_instance_metadata
        select * from ycloud_instance_metadata where metadata_endpoint="http://169.254.169.254"
    """
    instance_id = TextField(help_text="Unique identifier for the VM")  # {'index': True}
    folder_id = TextField(help_text="Folder identifier for the VM")
    name = TextField(help_text="Name of the VM")
    description = TextField(help_text="Description of the VM")
    hostname = TextField(help_text="Hostname of the VM")
    zone = TextField(help_text="Availability zone of the VM")
    ssh_public_key = TextField(help_text="SSH public key. Only available if supplied at instance launch time")
    serial_port_enabled = TextField(help_text="Indicates if serial port is enabled for the VM")
    metadata_endpoint = TextField(help_text="Endpoint used to fetch VM metadata")  # {'index': True}

    class Meta:
        table_name = "ycloud_instance_metadata"
