"""
Report Target functions
"""
from ..utils import Dispatch, exceptions

Report = Dispatch("report")


@Report.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()
