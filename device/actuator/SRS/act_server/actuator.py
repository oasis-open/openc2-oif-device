from .utils import ActuatorBase

from .actions import (
    Contain,
    Delete,
    Deny,
    Investigate,
    Locate,
    Query,
    Remediate,
    Scan
)


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Contain)
        self._dispatch.register_dispatch(Delete)
        self._dispatch.register_dispatch(Deny)
        self._dispatch.register_dispatch(Investigate)
        self._dispatch.register_dispatch(Locate)
        self._dispatch.register_dispatch(Query)
        self._dispatch.register_dispatch(Remediate)
        self._dispatch.register_dispatch(Scan)
