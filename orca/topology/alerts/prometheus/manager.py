from orca.topology.alerts import probe


def initialize_probes(graph):
    return [
        probe.Probe('prometheus', 'alert', graph=graph)]


def initialize_linkers(graph):
    return []
