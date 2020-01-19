from orca.topology.probes import extractor


class KubeExtractor(extractor.Extractor):

    def extract_id(self, entity):
        return entity.metadata.uid

    def extract_kind(self, entity):
        return entity.kind.lower()
