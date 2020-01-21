from orca.topology.probes import fetcher, synchronizer
from orca.topology.probes.k8s import fetcher as k8s_fetcher


class SynchronizerFactory(object):

    @staticmethod
    def get_synchronizer(graph, client, entity_kind, extractor):
        graph_fetcher = fetcher.GraphFetcher(graph, entity_kind)
        upstream_fetcher = k8s_fetcher.FetcherFactory.get_fetcher(client, entity_kind, extractor)
        return synchronizer.Synchronizer(graph, graph_fetcher, upstream_fetcher)
