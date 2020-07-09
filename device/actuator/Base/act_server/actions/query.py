"""
Query Target functions
"""
from sb_utils import FrozenDict
from ..utils import Dispatch, exceptions

Query = Dispatch("query")

Features = FrozenDict(
    pairs=lambda act: act.pairs,
    profiles=lambda act: act.profile,
    rate_limit=lambda act: getattr(act, "rate_limit", 0),
    versions=lambda act: act.schema.get("meta", {}).get("version", "N/A")
)


@Query.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Query.register
def features(act, target=[], args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - {"response"}) > 0:
        print("Invalid Query Args")
        return exceptions.bad_argument()

    if not isinstance(target, list) and len(set(target) - set(Features.keys())) > 0:
        return exceptions.bad_request()

    else:
        rtn = dict(
            status=200,
            results={k: Features[k](act) for k in target}
        )

        return {k: v for k, v in rtn.items() if v}
