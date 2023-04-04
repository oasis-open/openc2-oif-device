"""
OSQuery carbon_black_info ORM
"""
from ...orm import BaseModel
from peewee import IntegerField, TextField


class CarbonBlackInfo(BaseModel):
    """
    Returns info about a Carbon Black sensor install.
    """
    sensor_id = IntegerField(help_text="Sensor ID of the Carbon Black sensor")
    config_name = TextField(help_text="Sensor group")
    collect_store_files = IntegerField(help_text="If the sensor is configured to send back binaries to the Carbon Black server")
    collect_module_loads = IntegerField(help_text="If the sensor is configured to capture module loads")
    collect_module_info = IntegerField(help_text="If the sensor is configured to collect metadata of binaries")
    collect_file_mods = IntegerField(help_text="If the sensor is configured to collect file modification events")
    collect_reg_mods = IntegerField(help_text="If the sensor is configured to collect registry modification events")
    collect_net_conns = IntegerField(help_text="If the sensor is configured to collect network connections")
    collect_processes = IntegerField(help_text="If the sensor is configured to process events")
    collect_cross_processes = IntegerField(help_text="If the sensor is configured to cross process events")
    collect_emet_events = IntegerField(help_text="If the sensor is configured to EMET events")
    collect_data_file_writes = IntegerField(help_text="If the sensor is configured to collect non binary file writes")
    collect_process_user_context = IntegerField(help_text="If the sensor is configured to collect the user running a process")
    collect_sensor_operations = IntegerField(help_text="Unknown")
    log_file_disk_quota_mb = IntegerField(help_text="Event file disk quota in MB")
    log_file_disk_quota_percentage = IntegerField(help_text="Event file disk quota in a percentage")
    protection_disabled = IntegerField(help_text="If the sensor is configured to report tamper events")
    sensor_ip_addr = TextField(help_text="IP address of the sensor")
    sensor_backend_server = TextField(help_text="Carbon Black server")
    event_queue = IntegerField(help_text="Size in bytes of Carbon Black event files on disk")
    binary_queue = IntegerField(help_text="Size in bytes of binaries waiting to be sent to Carbon Black server")

    class Meta:
        table_name = "carbon_black_info"
