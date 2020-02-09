def match_namespace(node_a, node_b):
    return node_a.properties.namespace == node_b.properties.namespace


def match_selector(node, selector):
    labels = node.properties.labels
    if selector and labels:
        return all(item in labels.items() for item in selector.items())
    return False
