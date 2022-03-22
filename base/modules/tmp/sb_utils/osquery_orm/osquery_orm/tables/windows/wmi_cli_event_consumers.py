"""
OSQuery wmi_cli_event_consumers ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class WmiCliEventConsumers(BaseModel):
    """
    WMI CommandLineEventConsumer, which can be used for persistence on Windows. See https://www.blackhat.com/docs/us-15/materials/us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent%20Asynchronous-And-Fileless-Backdoor-wp.pdf for more details.
    Examples:
        select filter,consumer,query,command_line_template,wcec.name from wmi_cli_event_consumers wcec left outer join wmi_filter_consumer_binding wcb on consumer = wcec.relative_path left outer join wmi_event_filters wef on wef.relative_path = wcb.filter;
    """
    name = TextField(help_text="Unique name of a consumer.")
    command_line_template = TextField(help_text="Standard string template that specifies the process to be started. This property can be NULL, and the ExecutablePath property is used as the command line.")
    executable_path = TextField(help_text="Module to execute. The string can specify the full path and file name of the module to execute, or it can specify a partial name. If a partial name is specified, the current drive and current directory are assumed.")
    class_ = TextField(help_text="The name of the class.", column_name="class")
    relative_path = TextField(help_text="Relative path to the class or instance.")

    class Meta:
        table_name = "wmi_cli_event_consumers"
