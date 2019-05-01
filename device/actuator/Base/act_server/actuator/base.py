"""
Simple Actuator base class to dynamically load actions from hte actuator directory
"""
import json
import os
import uuid

from types import MethodType

from . import actions

from .utils import safe_load, FrozenDict


class Actuator(object):
    _ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
    _ACT_ID = str(uuid.uuid4())

    def __init__(self, root=_ROOT_DIR, act_id=_ACT_ID):
        """
        Initialize and start the Actuator Process
        :param act_id: id of the actuator
        """
        config_file = os.path.join(root, 'config.json')
        schema_file = os.path.join(root, 'schema.json')

        with open(config_file, 'r+' if os.path.isfile(config_file) else 'w+') as _conf:
            _config = safe_load(_conf)

            if len(_config.keys()) == 0:
                _config = dict(
                    actuator_id=act_id,
                    schema=safe_load(open(schema_file, 'r'))
                )
                json.dump(_config, _conf, indent=4, sort_keys=True)

            elif 'actuator_id' not in _config:
                _config['actuator_id'] = act_id
                json.dump(_config, _conf, indent=4, sort_keys=True)

            elif 'schema' not in _config:
                _config['schema'] = FrozenDict(safe_load(open(schema_file, 'r')))
                json.dump(_config, _conf, indent=4, sort_keys=True)

        self._config = FrozenDict(_config)
        self._profile = self._config.schema.get('meta', {}).get('title', 'N/A').replace(' ', '_').lower()
        del config_file, schema_file, _config

        self._pairs = {}
        self._valid_actions = ()
        self._valid_targets = ()

        # Get valid Actions & Targets from the schema
        # TODO: validate based on the schema format
        for key in ('Action', 'Target'):
            key_def = list(filter(lambda x: x[0] == key, self._config.schema.get('types', [])))
            if len(key_def) == 1:
                setattr(self, f'_valid_{key.lower()}s', tuple(a[1] for a in key_def[0][4]))
                del key_def
            elif len(key_def) == 0:
                raise ImportError(f'{key} type not defined in the schema')
            else:
                raise ImportError(f'Multiple {key} types defined in the schema')

        for act in actions.actions:
            if act in self._valid_actions:
                self._pairs[act] = actions.pairs.get(act, [])
                setattr(self, f'_{act}', MethodType(getattr(actions, act), self))
            del act

        self._pairs = FrozenDict(self._pairs)

    @property
    def profile(self):
        return self._profile

    @property
    def schema(self):
        return self._config.schema

    def action(self, msg):
        """
        Process command message
        :param msg: message instance
        :return: message results
        """
        # rename id - id is python method
        msg['cmd_id'] = msg['id']
        del msg['id']

        action = msg.get('action', 'action_not_implemented')
        if action in self._valid_actions:
            # TODO: should multiple targets be valid??
            target = list(msg.get('target', {}).keys())
            if len(target) == 1:
                if target[0] in self._valid_targets:
                    msg.setdefault("args", {}).setdefault("response_requested", "complete")
                    return getattr(self, f'_{action}', self._action_not_implemented)(**msg)
                else:
                    # Invalid target type
                    return self._action_exception(**msg, except_msg='Invalid target type')
            else:
                # Invalid target definition
                return self._action_exception(**msg, except_msg='Invalid target definition')
        else:
            # Invalid action
            return self._action_not_implemented(**msg, except_msg='Option not supported')

    def _action_not_implemented(self, cmd_id=0, action='ACTION', *args, **kwargs):
        """
        Default function if no action function is found
        :param cmd_id: id of the command
        :param action: action that is requested
        :param args: positional arguments passed to the function - list
        :param kwargs: keyword arguments passed to the function - dict
        :return: OpenC2 response message - dict
        """
        return dict(
            id=cmd_id,
            status=501,
            status_text=f'{action} action not implemented'
        )

    def _action_exception(self, cmd_id=0, action='ACTION', status=400, except_msg='', *args, **kwargs):
        """
        Action xception message creation for errors
        :param cmd_id: id of the command
        :param action: action that is requested
        :param status: status code of the error
        :param except_msg: message to return stating the error
        :param args: positional arguments passed to the function - list
        :param kwargs: keyword arguments passed to the function - dict
        :return: OpenC2 response message - dict
        """
        return dict(
            id=cmd_id,
            status=status,
            status_text=f'Invalid command for type {action}' if except_msg == '' else except_msg
        )

    def _server_exception(self, cmd_id=0, *args, **kwargs):
        """
        Server exception response
        :param cmd_id: id of the command
        :param args: positional arguments passed to the function - list
        :param kwargs: keyword arguments passed to the function - dict
        :return: OpenC2 response message - dict
        """
        return dict(
            id=cmd_id,
            status=500,
            status_text='Server Error. The server encountered an unexpected condition that prevented it from fulfilling the request'
        )

    def _bad_request(self, cmd_id=0, *args, **kwargs):
        """
        Bad Request exception response
        :param cmd_id: id of the command
        :param args: positional arguments passed to the function - list
        :param kwargs: keyword arguments passed to the function - dict
        :return: OpenC2 response message - dict
        """
        return dict(
            id=cmd_id,
            status=400,
            status_text='Bad Request. The server cannot process the request due to something that is perceived to be a client error (e.g., malformed request syntax.)'
        )
