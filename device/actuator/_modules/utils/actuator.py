"""
Simple Actuator base class to dynamically load actions from the Action Dispatch
"""
import json
import os
import uuid

from sb_utils import FrozenDict
from typing import Union

from . import exceptions

from .dispatch import Dispatch
from .general import safe_load


class ActuatorBase(object):
    _ROOT_DIR = os.getcwd()
    _ACT_ID = str(uuid.uuid4())

    def __init__(self, root: str = _ROOT_DIR, act_id: str = _ACT_ID):
        """
        Initialize and start the Actuator Process
        :param root: rood directory of actuator - default CWD
        :param act_id: id of the actuator - default UUIDv4
        """
        config_file = os.path.join(root, "config.json")
        schema_file = os.path.join(root, "schema.json")

        config = safe_load(open(config_file, "r" if os.path.isfile(config_file) else "w"))
        if len({"actuator_id", "schema"} - set(config.keys())) != 0:
            config.setdefault("actuator_id", act_id)
            config.setdefault("schema", safe_load(open(schema_file, "r")))
            json.dump(config, open(config_file, "w"), indent=4, sort_keys=True)

        self._config = FrozenDict(config)

        self._dispatch = Dispatch(act=self, dispatch_transform=self._dispatch_transform)
        self._dispatch.register(exceptions.action_not_implemented, "default")

        self._valid_actions = ()
        self._valid_targets = ()

        # Get valid Actions & Targets from the schema
        if len({"meta", "types"} - set(self._config.schema.keys())) == 0:  # JADN
            self._profile = self._config.schema.get("meta", {}).get("title", "N/A").replace(" ", "_").lower()

            for key in ("Action", "Target"):
                key_def = [x for x in self._config.schema.get("types", []) if x[0] == key]
                key_def = key_def[0] if len(key_def) == 1 else None
                if key_def:
                    setattr(self, f"_valid_{key.lower()}s", tuple(a[1] for a in key_def[4]))
                else:
                    raise KeyError(f"{key} not found in schema")
        else:  # JSON
            self._profile = self._config.schema.get("title", "N/A").replace(" ", "_").lower()

            schema_defs = self._config.schema.get("definitions", {})
            self._valid_actions = tuple(schema_defs.get("Action", {}).get("enum", []))

            targets = schema_defs.get("Target", {}).get("oneOf", [])
            self._valid_targets = tuple(k for t in targets for k in t.get("properties", {}).keys())

    @property
    def pairs(self) -> FrozenDict:
        pairs = {}
        for p in self._dispatch.registered:
            p = p.split(".")
            if "default" not in p:
                pairs.setdefault(p[0], []).append(p[1])

        return FrozenDict(pairs)

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def schema(self) -> FrozenDict:
        return self._config.schema

    def action(self, msg_id: Union[str, int] = None, msg: dict = {}) -> dict:
        """
        Process command message
        :param msg_id: ID of message
        :param msg: message instance
        :return: message results
        """
        msg.pop("id", None)
        msg.pop("cmd_id", None)

        action = msg.get("action", "action_not_implemented")
        targets = list(msg.get("target", {}).keys())

        if len(targets) == 1:
            return self._dispatch.dispatch(key=f"{action}.{targets[0]}", cmd_id=msg_id, **msg)
        else:
            return exceptions.bad_request()

    # Helper Functions
    def _dispatch_transform(self, *args, **kwargs):
        action = kwargs.get("action", "ACTION")
        target = kwargs.get("target", {})

        if len(target) == 1:
            kwargs["target"] = target[list(target.keys())[0]]
        else:
            return None, exceptions.action_exception(action, except_msg="Invalid target format")

        return args, kwargs
