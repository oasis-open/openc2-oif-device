"""
Update Target functions
"""
from sb_utils.actuator import Dispatch, exceptions

Update = Dispatch("update")


@Update.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Update.register
def file(target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - {"response_requested", "start_time"}) > 0:
        print("Invalid Update Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('update', except_msg='target implementation TBD')
