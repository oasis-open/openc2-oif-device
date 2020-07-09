"""
Simple Actuator base class to dynamically load actions from the Action Dispatch
"""
import json
import os
import uuid

from sb_utils import FrozenDict
from typing import (
    Tuple,
    Union
)

from . import (
    dispatch,
    exceptions,
    general
)


class ActuatorBase(object):
    _ROOT_DIR = os.getcwd()
    _ACT_ID = str(uuid.uuid4())

    def __init__(self, root: str = _ROOT_DIR, act_id: str = _ACT_ID) -> None:
        """
        Initialize and start the Actuator Process
        :param root: rood directory of actuator - default CWD
        :param act_id: id of the actuator - default UUIDv4
        """
        config_file = os.path.join(root, "config.json")
        schema_file = os.path.join(root, "schema.json")

        config = general.safe_load(config_file)
        if len({"actuator_id", "schema"} - set(config.keys())) != 0:
            config.setdefault("actuator_id", act_id)
            config.setdefault("schema", general.safe_load(schema_file))
            json.dump(config, open(config_file, "w"), indent=4)

        self._config = FrozenDict(config)
        self._dispatch = dispatch.Dispatch(act=self, dispatch_transform=self._dispatch_transform)
        self._dispatch.register(exceptions.action_not_implemented, "default")
        self._pairs = None

        # Get valid Actions & Targets from the schema
        self._profile = self._config.schema.get("title", "N/A").replace(" ", "_").lower()
        self._validator = general.ValidatorJSON(self._config.schema)

        schema_defs = self._config.schema.get("definitions", {})

        self._valid_actions = tuple(a["const"] for a in schema_defs.get("Action", {}).get("oneOf", []))
        self._valid_targets = tuple(schema_defs.get("Target", {}).get("properties", {}).keys())

    def __repr__(self) -> str:
        return f"Actuator({self.profile})"

    @property
    def pairs(self) -> FrozenDict:
        """
        Valid Action/Target pairs registered to this actuator instance
        :return: Action/Target Pairs
        """
        if self._pairs is None:
            pairs = {}
            for p in self._dispatch.registered:
                p = p.split(".")
                if "default" not in p:
                    pairs.setdefault(p[0], []).append(p[1])
            self._pairs = FrozenDict(pairs)
        return self._pairs

    @property
    def profile(self) -> str:
        """
        Profile this actuator is configured
        :return: actuator profile
        """
        return self._profile

    @property
    def schema(self) -> FrozenDict:
        """
        Schema this actuator is configured
        :return: actuator schema
        """
        return self._config.schema

    def action(self, msg_id: Union[str, int] = None, msg: dict = None) -> Union[dict, None]:
        """
        Process command message
        :param msg_id: ID of message
        :param msg: message instance
        :return: message results
        """
        msg = msg or {}
        errors = list(self._validator.iter_errors_as(msg, "OpenC2_Command"))
        val_cmd = len(errors) == 0

        if val_cmd:
            action = msg.get("action", "action_not_implemented")
            targets = list(msg.get("target", {}).keys())
            response_requested = msg.get("args", {}).get("response_requested", "complete")

            if len(targets) == 1:
                rtn = self._dispatch.dispatch(key=f"{action}.{targets[0]}", cmd_id=msg_id, **msg)
                return None if response_requested.lower() == "none" else rtn
            else:
                return exceptions.bad_request()
        else:
            print(f"Invalid Command - {msg} -> [{', '.join(getattr(e, 'message', e) for e in errors)}]")
            return exceptions.bad_request()

    # Helper Functions
    def _dispatch_transform(self, *args: tuple, **kwargs: dict) -> Tuple[Union[None, tuple], dict]:
        """
        Transform the command/message so the target is the value of the first key
        :param args: arguments to pass
        :param kwargs: key/value arguments - expanded command/message
        :return: args and transformed kwargs
        """
        action = kwargs.get("action", "ACTION")
        target = kwargs.get("target", {})

        if len(target) == 1:
            kwargs["target"] = target[list(target.keys())[0]]
        else:
            return None, exceptions.action_exception(action, except_msg="Invalid target format")

        return args, kwargs
