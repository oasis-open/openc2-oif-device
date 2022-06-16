"""
OSQuery docker_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DockerInfo(BaseModel):
    """
    Docker system information.
    Examples:
        select * from docker_info
    """
    id = TextField(help_text="Docker system ID")
    containers = IntegerField(help_text="Total number of containers")
    containers_running = IntegerField(help_text="Number of containers currently running")
    containers_paused = IntegerField(help_text="Number of containers in paused state")
    containers_stopped = IntegerField(help_text="Number of containers in stopped state")
    images = IntegerField(help_text="Number of images")
    storage_driver = TextField(help_text="Storage driver")
    memory_limit = IntegerField(help_text="1 if memory limit support is enabled. 0 otherwise")
    swap_limit = IntegerField(help_text="1 if swap limit support is enabled. 0 otherwise")
    kernel_memory = IntegerField(help_text="1 if kernel memory limit support is enabled. 0 otherwise")
    cpu_cfs_period = IntegerField(help_text="1 if CPU Completely Fair Scheduler (CFS) period support is enabled. 0 otherwise")
    cpu_cfs_quota = IntegerField(help_text="1 if CPU Completely Fair Scheduler (CFS) quota support is enabled. 0 otherwise")
    cpu_shares = IntegerField(help_text="1 if CPU share weighting support is enabled. 0 otherwise")
    cpu_set = IntegerField(help_text="1 if CPU set selection support is enabled. 0 otherwise")
    ipv4_forwarding = IntegerField(help_text="1 if IPv4 forwarding is enabled. 0 otherwise")
    bridge_nf_iptables = IntegerField(help_text="1 if bridge netfilter iptables is enabled. 0 otherwise")
    bridge_nf_ip6tables = IntegerField(help_text="1 if bridge netfilter ip6tables is enabled. 0 otherwise")
    oom_kill_disable = IntegerField(help_text="1 if Out-of-memory kill is disabled. 0 otherwise")
    logging_driver = TextField(help_text="Logging driver")
    cgroup_driver = TextField(help_text="Control groups driver")
    kernel_version = TextField(help_text="Kernel version")
    os = TextField(help_text="Operating system")
    os_type = TextField(help_text="Operating system type")
    architecture = TextField(help_text="Hardware architecture")
    cpus = IntegerField(help_text="Number of CPUs")
    memory = BigIntegerField(help_text="Total memory")
    http_proxy = TextField(help_text="HTTP proxy")
    https_proxy = TextField(help_text="HTTPS proxy")
    no_proxy = TextField(help_text="Comma-separated list of domain extensions proxy should not be used for")
    name = TextField(help_text="Name of the docker host")
    server_version = TextField(help_text="Server version")
    root_dir = TextField(help_text="Docker root directory")

    class Meta:
        table_name = "docker_info"
