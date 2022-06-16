"""
OSQuery osquery_packs ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class OsqueryPacks(BaseModel):
    """
    Information about the current query packs that are loaded in osquery.
    """
    name = TextField(help_text="The given name for this query pack")
    platform = TextField(help_text="Platforms this query is supported on")
    version = TextField(help_text="Minimum osquery version that this query will run on")
    shard = IntegerField(help_text="Shard restriction limit, 1-100, 0 meaning no restriction")
    discovery_cache_hits = IntegerField(help_text="The number of times that the discovery query used cached values since the last time the config was reloaded")
    discovery_executions = IntegerField(help_text="The number of times that the discovery queries have been executed since the last time the config was reloaded")
    active = IntegerField(help_text="Whether this pack is active (the version, platform and discovery queries match) yes=1, no=0.")

    class Meta:
        table_name = "osquery_packs"
