"""
Delete Target functions
"""
from ..utils import Dispatch

Delete = Dispatch("delete")


@Delete.register
def slpf_rule_number(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')
