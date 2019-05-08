"""
Report Target functions
"""
from ..utils import Dispatch

Report = Dispatch("report")


@Report.register
def default(act, *extra_args, **extra_kwargs):
    return act.action_exception(*extra_args, **extra_kwargs)
