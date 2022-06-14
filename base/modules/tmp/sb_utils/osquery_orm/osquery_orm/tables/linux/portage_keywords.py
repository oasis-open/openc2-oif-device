"""
OSQuery portage_keywords ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class PortageKeywords(BaseModel):
    """
    A summary about portage configurations like keywords, mask and unmask.
    """
    package = TextField(help_text="Package name")
    version = TextField(help_text="The version which are affected by the use flags, empty means all")
    keyword = TextField(help_text="The keyword applied to the package")
    mask = IntegerField(help_text="If the package is masked")
    unmask = IntegerField(help_text="If the package is unmasked")

    class Meta:
        table_name = "portage_keywords"
