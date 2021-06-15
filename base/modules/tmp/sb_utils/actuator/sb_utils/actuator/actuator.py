"""
Simple Actuator base class to dynamically load actions from the Action Dispatch
"""
import json
import os
import uuid
import etcd

from sb_utils import FrozenDict, safe_cast
from typing import Any, List, Optional, Tuple, Union
from . import dispatch, exceptions, general

# Constants
ROOT_DIR = os.getcwd()
ACT_ID = str(uuid.uuid4())


class ActuatorBase:
    # default set vats
    _prefix: str = '/actuator'

    # Dynamically set vars
    _config: FrozenDict
    _dispatch: dispatch.Dispatch
    _etcd: etcd.Client = None
    _pairs: FrozenDict
    _profile: str
    _valid_actions: Tuple[str, ...]
    _valid_targets: Tuple[str, ...]
    _validator: general.ValidatorJSON

    def __init__(self, root=ROOT_DIR, act_id=ACT_ID, enable_etcd=True) -> None:
        """
        Initialize and start the Actuator Process
        :param root: rood directory of actuator - default CWD
        :param act_id: id of the actuator - default UUIDv4
        """
        config_file = os.path.join(root, "config.json")
        schema_file = os.path.join(root, "schema.json")

        # Set config
        config = general.safe_load(config_file)
        if "actuator_id" not in config.keys():
            config.setdefault("actuator_id", act_id)
            json.dump(config, open(config_file, "w"), indent=4)
        self._config = FrozenDict(
            **config,
            schema=general.safe_load(schema_file)
        )

        # Configure Action/Target functions
        self._dispatch = dispatch.Dispatch(namespace="root",  dispatch_transform=self._dispatch_transform, act=self)
        self._dispatch.register(exceptions.action_not_implemented, "default")

        # Get valid Actions & Targets from the schema
        self._profile = self._config.schema.get("title", "N/A").replace(" ", "_").lower()
        self._validator = general.ValidatorJSON(self._config.schema)
        schema_defs = self._config.schema.get("definitions", {})
        self._valid_actions = tuple(a["const"] for a in schema_defs.get("Action", {}).get("oneOf", []))
        self._valid_targets = tuple(schema_defs.get("Target", {}).get("properties", {}).keys())

        # Initialize etcd client and set profiles
        if enable_etcd:
            self._etcd = etcd.Client(
                host=os.environ.get('ETCD_HOST', 'etcd'),
                port=safe_cast(os.environ.get('ETCD_PORT', 4001), int, 4001)
            )
            profiles = self.nsid if len(self.nsid) > 0 else [self._profile]
            for profile in profiles:
                self._etcd.write(f"{self._prefix}/{profile}", self._config.actuator_id)

    def __repr__(self) -> str:
        return f"Actuator({self._profile})"

    @property
    def nsid(self) -> List[str]:
        """
        NSID this actuator is configured
        :return: actuator nsid
        """
        return list(self._config.schema.get("definitions", {}).get("Actuator", {}).get("properties", {}).keys())

    @property
    def pairs(self) -> FrozenDict:
        """
        Valid Action/Target pairs registered to this actuator instance
        :return: Action/Target Pairs
        """
        if not hasattr(self, "_pairs"):
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

    def action(self, msg_id: Union[str, int] = None, msg: dict = None) -> Optional[dict]:
        """
        Process command message
        :param msg_id: ID of message
        :param msg: message instance
        :return: message results
        """
        msg = msg or {}
        errors = list(self._validator.iter_errors_as(msg, "OpenC2-Command"))

        if len(errors) == 0:
            action = msg.get("action", "action_not_implemented")
            targets = list(msg.get("target", {}).keys())
            response_requested = msg.get("args", {}).get("response_requested", "complete")

            if len(targets) == 1:
                rtn = self._dispatch.dispatch(key=f"{action}.{targets[0]}", cmd_id=msg_id, **msg)
                return None if response_requested.lower() == "none" else rtn
            return exceptions.bad_request()
        print(f"Invalid Command - {msg} -> [{', '.join(getattr(e, 'message', e) for e in errors)}]")
        return exceptions.bad_request()

    def _dispatch_transform(self, *args: Any, **kwargs: Union[dict, int, str]) -> Tuple[Union[None, tuple], dict]:
        # Helper Functions
        """
        Transform the command/message so the target is the value of the first key
        :param args: arguments to pass
        :param kwargs: key/value arguments - expanded command/message
        :return: args and transformed kwargs
        """
        target = kwargs.get("target", {})
        if len(target) == 1:
            kwargs["target"] = target[list(target.keys())[0]]
        else:
            action = kwargs.get("action", "ACTION")
            return None, exceptions.action_exception(action, except_msg="Invalid target format")
        return args, kwargs

    def shutdown(self) -> None:
        if self._etcd:
            for profile in self.nsid if len(self.nsid) > 0 else [self._profile]:
                self._etcd.delete(f"{self._prefix}/{profile}")
