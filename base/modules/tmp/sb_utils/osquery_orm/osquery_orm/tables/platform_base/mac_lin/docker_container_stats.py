"""
OSQuery docker_container_stats ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DockerContainerStats(BaseModel):
    """
    Docker container statistics. Queries on this table take at least one second.
    Examples:
        select * from docker_container_stats where id = 'de8cfdc74c850967'
        select * from docker_container_stats where id = 'de8cfdc74c850967fd3832e128f4d12e2d5476a4aea282734bfb7e57f66fce2f'
    """
    id = TextField(help_text="Container ID")  # {'index': True, 'required': True}
    name = TextField(help_text="Container name")  # {'index': True}
    pids = IntegerField(help_text="Number of processes")
    read = BigIntegerField(help_text="UNIX time when stats were read")
    preread = BigIntegerField(help_text="UNIX time when stats were last read")
    interval = BigIntegerField(help_text="Difference between read and preread in nano-seconds")
    disk_read = BigIntegerField(help_text="Total disk read bytes")
    disk_write = BigIntegerField(help_text="Total disk write bytes")
    num_procs = IntegerField(help_text="Number of processors")
    cpu_total_usage = BigIntegerField(help_text="Total CPU usage")
    cpu_kernelmode_usage = BigIntegerField(help_text="CPU kernel mode usage")
    cpu_usermode_usage = BigIntegerField(help_text="CPU user mode usage")
    system_cpu_usage = BigIntegerField(help_text="CPU system usage")
    online_cpus = IntegerField(help_text="Online CPUs")
    pre_cpu_total_usage = BigIntegerField(help_text="Last read total CPU usage")
    pre_cpu_kernelmode_usage = BigIntegerField(help_text="Last read CPU kernel mode usage")
    pre_cpu_usermode_usage = BigIntegerField(help_text="Last read CPU user mode usage")
    pre_system_cpu_usage = BigIntegerField(help_text="Last read CPU system usage")
    pre_online_cpus = IntegerField(help_text="Last read online CPUs")
    memory_usage = BigIntegerField(help_text="Memory usage")
    memory_max_usage = BigIntegerField(help_text="Memory maximum usage")
    memory_limit = BigIntegerField(help_text="Memory limit")
    network_rx_bytes = BigIntegerField(help_text="Total network bytes read")
    network_tx_bytes = BigIntegerField(help_text="Total network bytes transmitted")

    class Meta:
        table_name = "docker_container_stats"
