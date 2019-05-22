"""
Scan Target functions
"""
from ..utils import Dispatch, exceptions

Scan = Dispatch("scan")


@Scan.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()
