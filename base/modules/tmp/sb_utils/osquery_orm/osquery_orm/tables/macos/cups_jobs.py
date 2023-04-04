"""
OSQuery cups_jobs ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class CupsJobs(BaseModel):
    """
    Returns all completed print jobs from cups.
    """
    title = TextField(help_text="Title of the printed job")
    destination = TextField(help_text="The printer the job was sent to")
    user = TextField(help_text="The user who printed the job")
    format = TextField(help_text="The format of the print job")
    size = IntegerField(help_text="The size of the print job")
    completed_time = IntegerField(help_text="When the job completed printing")
    processing_time = IntegerField(help_text="How long the job took to process")
    creation_time = IntegerField(help_text="When the print request was initiated")

    class Meta:
        table_name = "cups_jobs"
