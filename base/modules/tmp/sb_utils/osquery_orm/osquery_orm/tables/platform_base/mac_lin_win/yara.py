"""
OSQuery yara ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Yara(BaseModel):
    """
    Track YARA matches for files or PIDs.
    Examples:
        select * from yara where path = '/etc/passwd'
        select * from yara where path LIKE '/etc/%'
        select * from yara where path = '/etc/passwd' and sigfile = '/etc/osquery/yara/test.yara'
        select * from yara where path = '/etc/passwd' and sigrule = 'rule always_true { condition: true }'
    """
    path = TextField(help_text="The path scanned")  # {'index': True, 'required': True}
    matches = TextField(help_text="List of YARA matches")
    count = IntegerField(help_text="Number of YARA matches")
    sig_group = TextField(help_text="Signature group used")  # {'additional': True}
    sigfile = TextField(help_text="Signature file used")  # {'additional': True}
    sigrule = TextField(help_text="Signature strings used")  # {'additional': True, 'hidden': True}
    strings = TextField(help_text="Matching strings")
    tags = TextField(help_text="Matching tags")
    sigurl = TextField(help_text="Signature url")  # {'additional': True, 'hidden': True}

    class Meta:
        table_name = "yara"
