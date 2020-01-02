"""
Contain Target functions
"""
from ..utils import Dispatch, exceptions

Contain = Dispatch("contain")


@Contain.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Contain.register(key="acdci_mrt:operator_location")
def operator_location(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
