from orca.common.clients.kiali import client as kiali
from orca.topology.infra.kiali import probe


def initialize_probes(graph):
    kiali_client = kiali.KialiClient.get(
        "http://kiali.istio-system:20001", username="admin", password="admin")

    return [
        probe.Probe(graph=graph, kiali_client=kiali_client)]


def initialize_linkers(graph):
    return []
