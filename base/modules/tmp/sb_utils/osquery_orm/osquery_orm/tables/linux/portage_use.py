"""
OSQuery portage_use ORM
"""
from osquery_orm.orm import BaseModel
from peewee import TextField


class PortageUse(BaseModel):
    """
    List of enabled portage USE values for specific package.
    """
    package = TextField(help_text="Package name")
    version = TextField(help_text="The version of the installed package")
    use = TextField(help_text="USE flag which has been enabled for package")

    class Meta:
        table_name = "portage_use"
