"""
OSQuery curl ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class Curl(BaseModel):
    """
    Perform an http request and return stats about it.
    Examples:
        select url, round_trip_time, response_code from curl where url = 'https://github.com/osquery/osquery'
    """
    url = TextField(help_text="The url for the request")  # {'required': True, 'index': True}
    method = TextField(help_text="The HTTP method for the request")
    user_agent = TextField(help_text="The user-agent string to use for the request")  # {'additional': True}
    response_code = IntegerField(help_text="The HTTP status code for the response")
    round_trip_time = BigIntegerField(help_text="Time taken to complete the request")
    bytes = BigIntegerField(help_text="Number of bytes in the response")
    result = TextField(help_text="The HTTP response body")

    class Meta:
        table_name = "curl"
