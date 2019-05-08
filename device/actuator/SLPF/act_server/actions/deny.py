"""
Deny Target functions
"""
from ..utils import Dispatch

Deny = Dispatch("deny")


@Deny.register
def ip_addr(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')


@Deny.register
def ip_connection(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')
