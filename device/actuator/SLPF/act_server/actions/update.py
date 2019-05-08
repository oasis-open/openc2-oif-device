"""
Update Target functions
"""
from ..utils import Dispatch

Update = Dispatch("update")


@Update.register
def file(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')
