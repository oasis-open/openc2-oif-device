"""
OSQuery carves ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Carves(BaseModel):
    """
    List the set of completed and in-progress carves. If carve=1 then the query is treated as a new carve request.
    Examples:
        select * from carves
        select * from carves where status like '%FAIL%'
        select * from carves where path like '/Users/%/Downloads/%' and carve=1
    """
    time = BigIntegerField(help_text="Time at which the carve was kicked off")
    sha256 = TextField(help_text="A SHA256 sum of the carved archive")
    size = IntegerField(help_text="Size of the carved archive")
    path = TextField(help_text="The path of the requested carve")  # {'additional': True}
    status = TextField(help_text="Status of the carve, can be STARTING, PENDING, SUCCESS, or FAILED")
    carve_guid = TextField(help_text="Identifying value of the carve session")  # {'index': True}
    request_id = TextField(help_text="Identifying value of the carve request (e.g., scheduled query name, distributed request, etc)")
    carve = IntegerField(help_text="Set this value to \'1\' to start a file carve")  # {'additional': True}

    class Meta:
        table_name = "carves"
