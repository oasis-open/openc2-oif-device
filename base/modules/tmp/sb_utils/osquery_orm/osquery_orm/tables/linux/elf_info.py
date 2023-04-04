"""
OSQuery elf_info ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class ElfInfo(BaseModel):
    """
    ELF file information.
    Examples:
        select * from elf_info where path = '/usr/bin/grep'
    """
    class_ = TextField(help_text="Class type, 32 or 64bit", column_name="class")
    abi = TextField(help_text="Section type")
    abi_version = IntegerField(help_text="Section virtual address in memory")
    type = TextField(help_text="Offset of section in file")
    machine = IntegerField(help_text="Machine type")
    version = IntegerField(help_text="Object file version")
    entry = BigIntegerField(help_text="Entry point address")
    flags = IntegerField(help_text="ELF header flags")
    path = TextField(help_text="Path to ELF file")  # {'required': True, 'index': True}

    class Meta:
        table_name = "elf_info"
