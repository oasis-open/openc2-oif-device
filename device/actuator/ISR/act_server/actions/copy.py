"""
Copy Target functions
"""
from ..utils import Dispatch, exceptions

Copy = Dispatch("copy")


@Copy.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()
