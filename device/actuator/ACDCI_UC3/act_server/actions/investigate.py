"""
Investigate Target functions
"""
from ..utils import Dispatch, exceptions

Investigate = Dispatch("investigate")


@Investigate.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Investigate.register
def device(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
