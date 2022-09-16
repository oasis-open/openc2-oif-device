"""
OSQuery quicklook_cache ORM
"""
from ...orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class QuicklookCache(BaseModel):
    """
    Files and thumbnails within OS X\'s Quicklook Cache.
    """
    path = TextField(help_text="Path of file")
    rowid = IntegerField(help_text="Quicklook file rowid key")
    fs_id = TextField(help_text="Quicklook file fs_id key")
    volume_id = IntegerField(help_text="Parsed volume ID from fs_id")
    inode = IntegerField(help_text="Parsed file ID (inode) from fs_id")
    mtime = IntegerField(help_text="Parsed version date field")
    size = BigIntegerField(help_text="Parsed version size field")
    label = TextField(help_text="Parsed version \'gen\' field")
    last_hit_date = IntegerField(help_text="Apple date format for last thumbnail cache hit")
    hit_count = TextField(help_text="Number of cache hits on thumbnail")
    icon_mode = BigIntegerField(help_text="Thumbnail icon mode")
    cache_path = TextField(help_text="Path to cache data")

    class Meta:
        table_name = "quicklook_cache"
