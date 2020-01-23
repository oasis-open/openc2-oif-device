"""
Create Target functions
"""
from ..utils import Dispatch, exceptions

Create = Dispatch("create")


@Create.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Create.register(key="acdci_mm:geospace")
def geospace(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )