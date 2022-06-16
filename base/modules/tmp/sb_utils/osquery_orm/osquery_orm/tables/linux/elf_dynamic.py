"""
OSQuery elf_dynamic ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class ElfDynamic(BaseModel):
    """
    ELF dynamic section information.
    Examples:
        select * from elf_dynamic where path = '/usr/bin/grep'
    """
    tag = IntegerField(help_text="Tag ID")
    value = IntegerField(help_text="Tag value")
    class_ = IntegerField(help_text="Class (32 or 64)", column_name="class")
    path = TextField(help_text="Path to ELF file")  # {'required': True, 'index': True}

    class Meta:
        table_name = "elf_dynamic"
