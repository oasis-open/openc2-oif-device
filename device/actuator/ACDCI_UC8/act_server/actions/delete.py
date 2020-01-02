"""
Delete Target functions
"""
from ..utils import Dispatch, exceptions

Delete = Dispatch("delete")


@Delete.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Delete.register(key="acdci_lw:drone")
def drone(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
