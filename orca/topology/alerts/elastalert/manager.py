from orca.topology.alerts import probe


def initialize_probes(graph):
    return [
        probe.Probe('elastalert', 'alert', graph=graph)]


def initialize_linkers(graph):
    return []
