"""
Deny Target functions
"""
from ..utils import Dispatch, exceptions

Deny = Dispatch("deny")


@Deny.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Deny.register(key="acdci_djs_geo:jamming_location")
def jamming_location(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
