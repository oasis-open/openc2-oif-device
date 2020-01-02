from .utils import ActuatorBase

from .actions import (
    Investigate,
    Query
)


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Investigate)
        self._dispatch.register_dispatch(Query)
