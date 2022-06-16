"""
OSQuery cpu_time ORM
"""
from osquery_orm.orm import BaseModel
from peewee import BigIntegerField, IntegerField


class CpuTime(BaseModel):
    """
    Displays information from /proc/stat file about the time the cpu cores spent in different parts of the system.
    """
    core = IntegerField(help_text="Name of the cpu (core)")
    user = BigIntegerField(help_text="Time spent in user mode")
    nice = BigIntegerField(help_text="Time spent in user mode with low priority (nice)")
    system = BigIntegerField(help_text="Time spent in system mode")
    idle = BigIntegerField(help_text="Time spent in the idle task")
    iowait = BigIntegerField(help_text="Time spent waiting for I/O to complete")
    irq = BigIntegerField(help_text="Time spent servicing interrupts")
    softirq = BigIntegerField(help_text="Time spent servicing softirqs")
    steal = BigIntegerField(help_text="Time spent in other operating systems when running in a virtualized environment")
    guest = BigIntegerField(help_text="Time spent running a virtual CPU for a guest OS under the control of the Linux kernel")
    guest_nice = BigIntegerField(help_text="Time spent running a niced guest ")

    class Meta:
        table_name = "cpu_time"
