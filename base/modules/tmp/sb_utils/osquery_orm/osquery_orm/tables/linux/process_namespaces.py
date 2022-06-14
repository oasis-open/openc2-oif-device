"""
OSQuery process_namespaces ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField, TextField


class ProcessNamespaces(BaseModel):
    """
    Linux namespaces for processes running on the host system.
    Examples:
        select * from process_namespaces where pid = 1
    """
    pid = IntegerField(help_text="Process (or thread) ID")  # {'index': True}
    cgroup_namespace = TextField(help_text="cgroup namespace inode")
    ipc_namespace = TextField(help_text="ipc namespace inode")
    mnt_namespace = TextField(help_text="mnt namespace inode")
    net_namespace = TextField(help_text="net namespace inode")
    pid_namespace = TextField(help_text="pid namespace inode")
    user_namespace = TextField(help_text="user namespace inode")
    uts_namespace = TextField(help_text="uts namespace inode")

    class Meta:
        table_name = "process_namespaces"
