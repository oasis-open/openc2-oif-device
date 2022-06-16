"""
OSQuery msr ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField


class Msr(BaseModel):
    """
    Various pieces of data stored in the model specific register per processor. NOTE: the msr kernel module must be enabled, and osquery must be run as root.
    """
    processor_number = BigIntegerField(help_text="The processor number as reported in /proc/cpuinfo")
    turbo_disabled = BigIntegerField(help_text="Whether the turbo feature is disabled.")
    turbo_ratio_limit = BigIntegerField(help_text="The turbo feature ratio limit.")
    platform_info = BigIntegerField(help_text="Platform information.")
    perf_ctl = BigIntegerField(help_text="Performance setting for the processor.")
    perf_status = BigIntegerField(help_text="Performance status for the processor.")
    feature_control = BigIntegerField(help_text="Bitfield controlling enabled features.")
    rapl_power_limit = BigIntegerField(help_text="Run Time Average Power Limiting power limit.")
    rapl_energy_status = BigIntegerField(help_text="Run Time Average Power Limiting energy status.")
    rapl_power_units = BigIntegerField(help_text="Run Time Average Power Limiting power units.")

    class Meta:
        table_name = "msr"
