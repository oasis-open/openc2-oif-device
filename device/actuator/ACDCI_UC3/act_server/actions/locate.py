"""
Locate Target functions
"""
from ..utils import Dispatch, exceptions

Locate = Dispatch("locate")


@Locate.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Locate.register(key='acdci_rft_dop:drone_team_df')
def drone_team_df(act, target=[], args={}, *extra_args, **extra_kwargs):
    # return exceptions.not_implemented()
    return dict(
        status=200
    )
