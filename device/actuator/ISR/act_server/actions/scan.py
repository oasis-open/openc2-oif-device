"""
Scan Target functions
"""
from ..utils import Dispatch

Scan = Dispatch("scan")


@Scan.register
def default(act, *extra_args, **extra_kwargs):
    return act.action_exception(*extra_args, **extra_kwargs)
