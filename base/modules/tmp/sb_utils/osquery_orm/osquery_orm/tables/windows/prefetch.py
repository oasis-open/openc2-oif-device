"""
OSQuery prefetch ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class Prefetch(BaseModel):
    """
    Prefetch files show metadata related to file execution.
    Examples:
        select * from prefetch;
    """
    path = TextField(help_text="Prefetch file path.")  # {'additional': True}
    filename = TextField(help_text="Executable filename.")
    hash = TextField(help_text="Prefetch CRC hash.")
    last_run_time = IntegerField(help_text="Most recent time application was run.")
    other_run_times = TextField(help_text="Other execution times in prefetch file.")
    run_count = IntegerField(help_text="Number of times the application has been run.")
    size = IntegerField(help_text="Application file size.")
    volume_serial = TextField(help_text="Volume serial number.")
    volume_creation = TextField(help_text="Volume creation time.")
    accessed_files_count = IntegerField(help_text="Number of files accessed.")
    accessed_directories_count = IntegerField(help_text="Number of directories accessed.")
    accessed_files = TextField(help_text="Files accessed by application within ten seconds of launch.")
    accessed_directories = TextField(help_text="Directories accessed by application within ten seconds of launch.")

    class Meta:
        table_name = "prefetch"
