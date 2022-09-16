"""
OSQuery elf_symbols ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class ElfSymbols(BaseModel):
    """
    ELF symbol list.
    Examples:
        select * from elf_symbols where path = '/usr/bin/grep'
    """
    name = TextField(help_text="Symbol name")
    addr = IntegerField(help_text="Symbol address (value)")
    size = IntegerField(help_text="Size of object")
    type = TextField(help_text="Symbol type")
    binding = TextField(help_text="Binding type")
    offset = IntegerField(help_text="Section table index")
    table = TextField(help_text="Table name containing symbol")
    path = TextField(help_text="Path to ELF file")  # {'required': True, 'index': True}

    class Meta:
        table_name = "elf_symbols"
