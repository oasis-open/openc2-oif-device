def openc2(self, cmd_id=0, target={}, *extra_args, **extra_kwargs):
    if len(target) != 1:
        return self._action_exception(cmd_id, 'query', except_msg='Invalid target type for action')

    valid_qry_itms = ['pairs', 'profiles', 'schema', 'versions']

    results = {}
    for qry_itm in target:
        if qry_itm not in valid_qry_itms:
            return self._bad_request(cmd_id)

        if qry_itm == 'pairs':
            results['pairs'] = [[act, tar] for act, tar in self._pairs.items()]

        elif qry_itm == 'profiles':
            results['profiles'] = self._profile

        elif qry_itm == 'schema':
            results['schema'] = self._config.schema

        elif qry_itm == 'versions':
            results['versions'] = self._config.schema.get('meta', {}).get('version', 'N/A')

    return dict(
        id=cmd_id,
        status=200,
        status_text='Ok, The request has succeeded.',
        results=results
    )