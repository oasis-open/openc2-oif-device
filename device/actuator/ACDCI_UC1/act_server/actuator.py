from .actions import (
    Query,
    Scan
)
from .utils import ActuatorBase


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Query)
        self._dispatch.register_dispatch(Scan)
