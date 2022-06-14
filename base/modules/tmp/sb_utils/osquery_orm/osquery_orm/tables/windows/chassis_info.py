"""
OSQuery chassis_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class ChassisInfo(BaseModel):
    """
    Display information pertaining to the chassis and its security status.
    Examples:
        select * from chassis_info
    """
    audible_alarm = TextField(help_text="If TRUE, the frame is equipped with an audible alarm.")
    breach_description = TextField(help_text="If provided, gives a more detailed description of a detected security breach.")
    chassis_types = TextField(help_text="A comma-separated list of chassis types, such as Desktop or Laptop.")
    description = TextField(help_text="An extended description of the chassis if available.")
    lock = TextField(help_text="If TRUE, the frame is equipped with a lock.")
    manufacturer = TextField(help_text="The manufacturer of the chassis.")
    model = TextField(help_text="The model of the chassis.")
    security_breach = TextField(help_text="The physical status of the chassis such as Breach Successful, Breach Attempted, etc.")
    serial = TextField(help_text="The serial number of the chassis.")
    smbios_tag = TextField(help_text="The assigned asset tag number of the chassis.")
    sku = TextField(help_text="The Stock Keeping Unit number if available.")
    status = TextField(help_text="If available, gives various operational or nonoperational statuses such as OK, Degraded, and Pred Fail.")
    visible_alarm = TextField(help_text="If TRUE, the frame is equipped with a visual alarm.")

    class Meta:
        table_name = "chassis_info"
