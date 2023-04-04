"""
OSQuery elf_sections ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class ElfSections(BaseModel):
    """
    ELF section information.
    Examples:
        select * from elf_sections where path = '/usr/bin/grep'
    """
    name = TextField(help_text="Section name")
    type = IntegerField(help_text="Section type")
    vaddr = IntegerField(help_text="Section virtual address in memory")
    offset = IntegerField(help_text="Offset of section in file")
    size = IntegerField(help_text="Size of section")
    flags = TextField(help_text="Section attributes")
    link = TextField(help_text="Link to other section")
    align = IntegerField(help_text="Segment alignment")
    path = TextField(help_text="Path to ELF file")  # {'required': True, 'index': True}

    class Meta:
        table_name = "elf_sections"
