from orca.topology.probes import linker


class Linker(linker.Linker):

    """Base class for Kubernetes entity linkers."""


class Matcher(linker.Matcher):

    def _match_namespace(self, node_a, node_b):
        return node_a.properties.namespace == node_b.properties.namespace

    def _match_selector(self, node, selector):
        labels = node.properties.labels
        if selector and labels:
            return all(item in labels.items() for item in selector.items())
        return False
