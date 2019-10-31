import random


def generate(num_nodes=10, num_masters=3, num_deployments=3,
             pods_per_deployment=2):
    distance = 100
    strength = 0.3

    graph_nodes = []
    graph_links = []

    graph_nodes.append(
        {'id': "cluster-0", 'label': "CLUSTER"})

    # nodes
    for i in range(num_nodes):
        graph_nodes.append(
            {'id': "node-%i" % i,
             'label': "NODE",
             'group': 0, 'level': 1})
        graph_links.append(
            {'target': "cluster-0",
             'source': "node-%i" % i,
             'strength': strength,
             'distance': distance})

    # master nodes
    for i in range(num_masters):
        graph_nodes.append(
            {'id': "master-%i" % i,
             'label': "MASTER",
             'group': 0,
             'level': 1})
        graph_links.append(
            {'target': "node-%i" % i,
             'source': "master-%i" % i,
             'strength': strength, 'distance': distance})

    # worker nodes
    for i in range(num_masters, num_nodes):
        graph_nodes.append(
            {'id': "worker-%i" % i,
             'label': "WORKER",
             'group': 0,
             'level': 1})
        graph_links.append(
            {'target': "node-%i" % i,
             'source': "worker-%i" % i,
             'strength': strength,
             'distance': distance})

    # deployments
    for i in range(num_deployments):
        deployment_id = "deployment-%i" % i
        service_id = "service-%i" % i
        graph_nodes.append(
            {'id': deployment_id,
             'label': "SERVICE",
             'group': 0,
             'level': 1})
        graph_nodes.append(
            {'id': service_id,
             'label': "DEPLOYMENT",
             'group': 0,
             'level': 1})
        for j in range(pods_per_deployment):
            pod_id = "pod-%i%i" % (i, j)
            graph_nodes.append(
                {'id': pod_id,
                 'label': "POD",
                 'group': 0,
                 'level': 1})
            graph_links.append(
                {'target': pod_id,
                 'source': deployment_id,
                 'strength': strength,
                 'distance': distance})
            graph_links.append(
                {'target': pod_id,
                 'source': service_id,
                 'strength': strength,
                 'distance': distance})
            worker_node_num = random.randint(num_masters, num_nodes - 1)
            worker_id = "worker-%i" % worker_node_num
            graph_links.append(
                {'target': worker_id,
                 'source': pod_id,
                 'strength': strength,
                 'distance': distance})

    return (graph_nodes, graph_links)
