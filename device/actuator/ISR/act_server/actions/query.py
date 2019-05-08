"""
Query Target functions
"""
from ..utils import Dispatch

Query = Dispatch("query")


@Query.register
def default(act, *extra_args, **extra_kwargs):
    return act.action_exception(*extra_args, **extra_kwargs)


@Query.register
def openc2(act, target={}, *extra_args, **extra_kwargs):
    if len(target) != 1:
        return act.action_exception('query', except_msg='Invalid target type for action')
    else:
        target = target[list(target.keys())[0]]

    valid_qry_itms = ['pairs', 'profiles', 'schema', 'versions']

    results = {}
    for qry_itm in target:
        if qry_itm not in valid_qry_itms:
            return act.bad_request()

        if qry_itm == 'pairs':
            results['pairs'] = [[act, tar] for act, tar in act.pairs.items()]

        elif qry_itm == 'profiles':
            results['profiles'] = act.profile

        elif qry_itm == 'schema':
            results['schema'] = act._config.schema

        elif qry_itm == 'versions':
            results['versions'] = act._config.schema.get('meta', {}).get('version', 'N/A')

    return dict(
        status=200,
        status_text='Ok, The request has succeeded.',
        results=results
    )
