"""
Copy Target functions
"""
from ..utils import Dispatch

Copy = Dispatch("copy")


@Copy.register
def default(act, *extra_args, **extra_kwargs):
    return act.action_exception(*extra_args, **extra_kwargs)
