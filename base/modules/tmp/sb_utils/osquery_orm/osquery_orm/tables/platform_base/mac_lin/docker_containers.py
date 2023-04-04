"""
OSQuery docker_containers ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, IntegerField, TextField


class DockerContainers(BaseModel):
    """
    Docker containers information.
    Examples:
        select * from docker_containers where id = '11b2399e1426d906e62a0c357650e363426d6c56dbe2f35cbaa9b452250e3355'
        select * from docker_containers where name = '/hello'
    """
    id = TextField(help_text="Container ID")  # {'index': True}
    name = TextField(help_text="Container name")  # {'index': True}
    image = TextField(help_text="Docker image (name) used to launch this container")
    image_id = TextField(help_text="Docker image ID")
    command = TextField(help_text="Command with arguments")
    created = BigIntegerField(help_text="Time of creation as UNIX time")
    state = TextField(help_text="Container state (created, restarting, running, removing, paused, exited, dead)")
    status = TextField(help_text="Container status information")
    pid = BigIntegerField(help_text="Identifier of the initial process")
    path = TextField(help_text="Container path")
    config_entrypoint = TextField(help_text="Container entrypoint(s)")
    started_at = TextField(help_text="Container start time as string")
    finished_at = TextField(help_text="Container finish time as string")
    privileged = IntegerField(help_text="Is the container privileged")
    security_options = TextField(help_text="List of container security options")
    env_variables = TextField(help_text="Container environmental variables")
    readonly_rootfs = IntegerField(help_text="Is the root filesystem mounted as read only")

    class Meta:
        table_name = "docker_containers"


# OS specific properties for Linux
class Linux_DockerContainers(DockerContainers):
    cgroup_namespace = TextField(help_text="cgroup namespace")
    ipc_namespace = TextField(help_text="IPC namespace")
    mnt_namespace = TextField(help_text="Mount namespace")
    net_namespace = TextField(help_text="Network namespace")
    pid_namespace = TextField(help_text="PID namespace")
    user_namespace = TextField(help_text="User namespace")
    uts_namespace = TextField(help_text="UTS namespace")

    class Meta:
        table_name = "docker_containers"
