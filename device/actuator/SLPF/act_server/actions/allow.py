"""
Allow Target functions
"""
from ..utils import Dispatch

Allow = Dispatch("allow")


@Allow.register
def default(act, *extra_args, **extra_kwargs):
    return act.action_exception(*extra_args, **extra_kwargs)


@Allow.register
def ip_addr(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')


@Allow.register
def ip_connection(act, target={}, *extra_args, **extra_kwargs):
    return act.action_exception('file', except_msg='target implementation TBD')

