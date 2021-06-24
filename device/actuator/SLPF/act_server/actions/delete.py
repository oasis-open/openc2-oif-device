"""
Delete Target functions
"""
from sb_utils.actuator import Dispatch, exceptions

Delete = Dispatch("delete")


@Delete.register
def default(act, *extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Delete.register
def slpf(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - {"response_requested", "start_time"}) > 0:
        print("Invalid Delete Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('delete', except_msg='target implementation TBD')
