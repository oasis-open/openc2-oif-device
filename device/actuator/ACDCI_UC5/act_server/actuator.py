from .actions import (
    Contain,
    Query
)
from .utils import ActuatorBase


class Actuator(ActuatorBase):
    def __init__(self, *args, **kwargs):
        super(Actuator, self).__init__(*args, **kwargs)
        self._dispatch.register_dispatch(Contain)
        self._dispatch.register_dispatch(Query)
