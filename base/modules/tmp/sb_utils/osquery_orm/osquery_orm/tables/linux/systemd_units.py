"""
OSQuery systemd_units ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, TextField


class SystemdUnits(BaseModel):
    """
    Track systemd units.
    """
    id = TextField(help_text="Unique unit identifier")
    description = TextField(help_text="Unit description")
    load_state = TextField(help_text="Reflects whether the unit definition was properly loaded")
    active_state = TextField(help_text="The high-level unit activation state, i.e. generalization of SUB")
    sub_state = TextField(help_text="The low-level unit activation state, values depend on unit type")
    following = TextField(help_text="The name of another unit that this unit follows in state")
    object_path = TextField(help_text="The object path for this unit")
    job_id = BigIntegerField(help_text="Next queued job id")
    job_type = TextField(help_text="Job type")
    job_path = TextField(help_text="The object path for the job")
    fragment_path = TextField(help_text="The unit file path this unit was read from, if there is any")
    user = TextField(help_text="The configured user, if any")
    source_path = TextField(help_text="Path to the (possibly generated) unit configuration file")

    class Meta:
        table_name = "systemd_units"
