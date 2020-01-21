import abc

import cotyledon

from orca.common import logger

log = logger.get_logger(__name__)


class ProbeService(cotyledon.Service):

    def __init__(self, service_id, probe):
        super().__init__(service_id)
        self._service_id = service_id
        self._probe = probe

    def run(self):
        self._probe.run()


class Probe(abc.ABC):

    def __init__(self, entity_kind):
        self._entity_kind = entity_kind

    @abc.abstractmethod
    def run(self):
        """Starts entity probe."""


class GraphProbe(Probe):

    def __init__(self, entity_kind, graph):
        super().__init__(entity_kind)
        self._graph = graph

    @abc.abstractmethod
    def run(self):
        """Starts graph probe."""
