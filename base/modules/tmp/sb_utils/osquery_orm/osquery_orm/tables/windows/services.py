"""
OSQuery services ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Services(BaseModel):
    """
    Lists all installed Windows services and their relevant data.
    Examples:
        select * from services
    """
    name = TextField(help_text="Service name")
    service_type = TextField(help_text="Service Type: OWN_PROCESS, SHARE_PROCESS and maybe Interactive (can interact with the desktop)")
    display_name = TextField(help_text="Service Display name")
    status = TextField(help_text="Service Current status: STOPPED, START_PENDING, STOP_PENDING, RUNNING, CONTINUE_PENDING, PAUSE_PENDING, PAUSED")
    pid = IntegerField(help_text="the Process ID of the service")
    start_type = TextField(help_text="Service start type: BOOT_START, SYSTEM_START, AUTO_START, DEMAND_START, DISABLED")
    win32_exit_code = IntegerField(help_text="The error code that the service uses to report an error that occurs when it is starting or stopping")
    service_exit_code = IntegerField(help_text="The service-specific error code that the service returns when an error occurs while the service is starting or stopping")
    path = TextField(help_text="Path to Service Executable")
    module_path = TextField(help_text="Path to ServiceDll")
    description = TextField(help_text="Service Description")
    user_account = TextField(help_text="The name of the account that the service process will be logged on as when it runs. This name can be of the form Domain\\UserName. If the account belongs to the built-in domain, the name can be of the form .\\UserName.")

    class Meta:
        table_name = "services"
