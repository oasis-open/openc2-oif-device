"""
Remediate Target functions
"""
from ..utils import Dispatch, exceptions

Remediate = Dispatch("remediate")


@Remediate.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Remediate.register(key="acdci_dcs:drone")
def drone(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
