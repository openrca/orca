import cotyledon


class Probe(cotyledon.Service):

    def __init__(self, probe_id):
        super().__init__(probe_id)
        self._probe_id = probe_id
