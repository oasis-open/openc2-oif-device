"""
Query Target functions
"""
from ..utils import Dispatch

Query = Dispatch("query")


@Query.register
def features(act, target={}, *extra_args, **extra_kwargs):
    if len(target) != 1:
        return act.action_exception('query', except_msg='Invalid target type for action')
    else:
        target = target[list(target.keys())[0]]

    valid_qry_itms = ['pairs', 'profiles', 'rate_limit', 'schema', 'versions']

    results = {}
    for qry_itm in target:
        if qry_itm not in valid_qry_itms:
            return act.bad_request()

        if qry_itm == 'pairs':
            results['pairs'] = [[act, tar] for act, tar in act._pairs.items()]
        else:
            results[qry_itm] = act._config.schema.get(qry_itm, '')

    return dict(
        status=200,
        status_text='Ok, The request has succeeded.',
        results=results
    )
