from orca.topology.infra.k8s import extractor


class Extractor(extractor.Extractor):

    def get_origin(self):
        return 'istio'
