from .actions import (
    Investigate,
    Query
)
from .utils import ActuatorBase


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Investigate)
        self._dispatch.register_dispatch(Query)
