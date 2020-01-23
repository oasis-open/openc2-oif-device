from .utils import ActuatorBase

from .actions import (
    Copy,
    Locate,
    Query,
    Report,
    Scan
)


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Copy)
        self._dispatch.register_dispatch(Locate)
        self._dispatch.register_dispatch(Query)
        self._dispatch.register_dispatch(Report)
        self._dispatch.register_dispatch(Scan)
