"""
OSQuery socket_events ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class SocketEvents(BaseModel):
    """
    Track network socket opens and closes.
    """
    action = TextField(help_text="The socket action (bind, listen, close)")
    pid = BigIntegerField(help_text="Process (or thread) ID")
    path = TextField(help_text="Path of executed file")
    fd = TextField(help_text="The file description for the process socket")
    auid = BigIntegerField(help_text="Audit User ID")
    status = TextField(help_text="Either \'succeeded\', \'failed\', \'in_progress\' (connect() on non-blocking socket) or \'no_client\' (null accept() on non-blocking socket)")
    family = IntegerField(help_text="The Internet protocol family ID")
    protocol = IntegerField(help_text="The network protocol ID")  # {'hidden': True}
    local_address = TextField(help_text="Local address associated with socket")
    remote_address = TextField(help_text="Remote address associated with socket")
    local_port = IntegerField(help_text="Local network protocol port number")
    remote_port = IntegerField(help_text="Remote network protocol port number")
    socket = TextField(help_text="The local path (UNIX domain socket only)")  # {'hidden': True}
    time = BigIntegerField(help_text="Time of execution in UNIX time")
    uptime = BigIntegerField(help_text="Time of execution in system uptime")
    eid = TextField(help_text="Event ID")  # {'hidden': True}
    success = IntegerField(help_text="Deprecated. Use the \'status\' column instead")  # {'hidden': True}

    class Meta:
        table_name = "socket_events"
