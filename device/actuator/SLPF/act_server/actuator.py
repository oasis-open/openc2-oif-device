from actions import (
    Allow,
    Delete,
    Deny,
    Query,
    Update
)
from sb_utils.actuator import ActuatorBase


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Allow)
        self._dispatch.register_dispatch(Delete)
        self._dispatch.register_dispatch(Deny)
        self._dispatch.register_dispatch(Query)
        self._dispatch.register_dispatch(Update)
