"""
Remediate Target functions
"""
from ..utils import Dispatch, exceptions

Remediate = Dispatch("remediate")


@Remediate.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Remediate.register
def device(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
