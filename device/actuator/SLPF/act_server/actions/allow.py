"""
Allow Target functions
"""
from ..utils import Dispatch, exceptions

Allow = Dispatch("allow")

ValidArgs = {
    "response",
    "start-time",
    "end-time",
    "duration",
    "running",
    "direction",
    "insert_rule",
}


@Allow.register
def default(act, *extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Allow.register
def ip_addr(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('allow', except_msg='target implementation TBD')


@Allow.register
def ip_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('allow', except_msg='target implementation TBD')

