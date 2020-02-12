from orca.topology.alerts import probe


def initialize_probes(graph):
    return [
        probe.Probe(graph=graph, origin='elastalert', kind='alert')]


def initialize_linkers(graph):
    return []
