"""
Deny Target functions
"""
from ..utils import Dispatch, exceptions

Deny = Dispatch("deny")


@Deny.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()
