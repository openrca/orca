import cotyledon


class Probe(cotyledon.Service):

    def __init__(self, worker_id):
        super().__init__(worker_id)
        self._worker_id = worker_id

