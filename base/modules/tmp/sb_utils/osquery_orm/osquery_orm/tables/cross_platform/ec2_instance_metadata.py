"""
OSQuery ec2_instance_metadata ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class Ec2InstanceMetadata(BaseModel):
    """
    EC2 instance metadata.
    Examples:
        select * from ec2_instance_metadata
    """
    instance_id = TextField(help_text="EC2 instance ID")
    instance_type = TextField(help_text="EC2 instance type")
    architecture = TextField(help_text="Hardware architecture of this EC2 instance")
    region = TextField(help_text="AWS region in which this instance launched")
    availability_zone = TextField(help_text="Availability zone in which this instance launched")
    local_hostname = TextField(help_text="Private IPv4 DNS hostname of the first interface of this instance")
    local_ipv4 = TextField(help_text="Private IPv4 address of the first interface of this instance")
    mac = TextField(help_text="MAC address for the first network interface of this EC2 instance")
    security_groups = TextField(help_text="Comma separated list of security group names")
    iam_arn = TextField(help_text="If there is an IAM role associated with the instance, contains instance profile ARN")
    ami_id = TextField(help_text="AMI ID used to launch this EC2 instance")
    reservation_id = TextField(help_text="ID of the reservation")
    account_id = TextField(help_text="AWS account ID which owns this EC2 instance")
    ssh_public_key = TextField(help_text="SSH public key. Only available if supplied at instance launch time")

    class Meta:
        table_name = "ec2_instance_metadata"
