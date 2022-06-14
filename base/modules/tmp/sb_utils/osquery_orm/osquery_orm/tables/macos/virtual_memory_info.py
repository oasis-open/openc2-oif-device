"""
OSQuery virtual_memory_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField


class VirtualMemoryInfo(BaseModel):
    """
    Darwin Virtual Memory statistics.
    Examples:
        select * from virtual_memory_info;
    """
    free = BigIntegerField(help_text="Total number of free pages.")
    active = BigIntegerField(help_text="Total number of active pages.")
    inactive = BigIntegerField(help_text="Total number of inactive pages.")
    speculative = BigIntegerField(help_text="Total number of speculative pages.")
    throttled = BigIntegerField(help_text="Total number of throttled pages.")
    wired = BigIntegerField(help_text="Total number of wired down pages.")
    purgeable = BigIntegerField(help_text="Total number of purgeable pages.")
    faults = BigIntegerField(help_text="Total number of calls to vm_faults.")
    copy = BigIntegerField(help_text="Total number of copy-on-write pages.")
    zero_fill = BigIntegerField(help_text="Total number of zero filled pages.")
    reactivated = BigIntegerField(help_text="Total number of reactivated pages.")
    purged = BigIntegerField(help_text="Total number of purged pages.")
    file_backed = BigIntegerField(help_text="Total number of file backed pages.")
    anonymous = BigIntegerField(help_text="Total number of anonymous pages.")
    uncompressed = BigIntegerField(help_text="Total number of uncompressed pages.")
    compressor = BigIntegerField(help_text="The number of pages used to store compressed VM pages.")
    decompressed = BigIntegerField(help_text="The total number of pages that have been decompressed by the VM compressor.")
    compressed = BigIntegerField(help_text="The total number of pages that have been compressed by the VM compressor.")
    page_ins = BigIntegerField(help_text="The total number of requests for pages from a pager.")
    page_outs = BigIntegerField(help_text="Total number of pages paged out.")
    swap_ins = BigIntegerField(help_text="The total number of compressed pages that have been swapped out to disk.")
    swap_outs = BigIntegerField(help_text="The total number of compressed pages that have been swapped back in from disk.")

    class Meta:
        table_name = "virtual_memory_info"
