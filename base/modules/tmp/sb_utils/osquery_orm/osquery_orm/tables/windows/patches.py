"""
OSQuery patches ORM
"""
from ...orm import BaseModel
from peewee import TextField


class Patches(BaseModel):
    """
    Lists all the patches applied. Note: This does not include patches applied via MSI or downloaded from Windows Update (e.g. Service Packs).
    Examples:
        select * from patches
    """
    csname = TextField(help_text="The name of the host the patch is installed on.")
    hotfix_id = TextField(help_text="The KB ID of the patch.")
    caption = TextField(help_text="Short description of the patch.")
    description = TextField(help_text="Fuller description of the patch.")
    fix_comments = TextField(help_text="Additional comments about the patch.")
    installed_by = TextField(help_text="The system context in which the patch as installed.")
    install_date = TextField(help_text="Indicates when the patch was installed. Lack of a value does not indicate that the patch was not installed.")
    installed_on = TextField(help_text="The date when the patch was installed.")

    class Meta:
        table_name = "patches"
