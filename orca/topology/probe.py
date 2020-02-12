import abc

import cotyledon


class ProbeService(cotyledon.Service):

    def __init__(self, service_id, probe):
        super().__init__(service_id)
        self._service_id = service_id
        self._probe = probe

    def run(self):
        self._probe.run()


class Probe(abc.ABC):

    def __init__(self, origin, kind, graph):
        super().__init__()
        self._origin = origin
        self._kind = kind
        self._graph = graph

    @property
    def _extended_kind(self):
        return "%s/%s" % (self._origin, self._kind)

    @abc.abstractmethod
    def run(self):
        """Starts entity probe."""
