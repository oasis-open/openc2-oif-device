"""
Deny Target functions
"""
from ..utils import Dispatch, exceptions

Deny = Dispatch("deny")

ValidArgs = {
    "response",
    "start-time",
    "end-time",
    "duration",
    "running",
    "direction",
    "insert_rule",
    "drop_process",
}


@Deny.register
def default(act, *extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Deny.register
def ip_addr(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('deny', except_msg='target implementation TBD')


@Deny.register
def ip_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('deny', except_msg='target implementation TBD')
