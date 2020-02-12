from orca.topology.infra.k8s import extractor


class Extractor(extractor.Extractor):

    def _extract_origin(self, entity):
        return "istio"
