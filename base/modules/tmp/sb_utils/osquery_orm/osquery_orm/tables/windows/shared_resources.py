"""
OSQuery shared_resources ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class SharedResources(BaseModel):
    """
    Displays shared resources on a computer system running Windows. This may be a disk drive, printer, interprocess communication, or other sharable device.
    Examples:
        select * from shared_resources
    """
    description = TextField(help_text="A textual description of the object")
    install_date = TextField(help_text="Indicates when the object was installed. Lack of a value does not indicate that the object is not installed.")
    status = TextField(help_text="String that indicates the current status of the object.")
    allow_maximum = IntegerField(help_text="Number of concurrent users for this resource has been limited. If True, the value in the MaximumAllowed property is ignored.")
    maximum_allowed = IntegerField(help_text="Limit on the maximum number of users allowed to use this resource concurrently. The value is only valid if the AllowMaximum property is set to FALSE.")
    name = TextField(help_text="Alias given to a path set up as a share on a computer system running Windows.")
    path = TextField(help_text="Local path of the Windows share.")
    type = IntegerField(help_text="Type of resource being shared. Types include: disk drives, print queues, interprocess communications (IPC), and general devices.")

    class Meta:
        table_name = "shared_resources"
