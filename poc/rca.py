import math
import multiprocessing

import networkx as nx
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import graphviz

from orca.graph import graph
from orca.common.clients.prometheus import client as prometheus
from orca.common import utils


time_point = 1615313740
start = 1615313659
end = 1615313779
sampling = 10

lock = multiprocessing.Lock()
dep_graph = graph.Graph.get(lock)

prom_client = prometheus.PrometheusClient.get(
    url="http://localhost:9090")


def main():
    nodes, links = get_dep_graph(time_point)
    nx_graph = build_nx_graph(nodes, links)

    alerts = filter_graph_nodes(nx_graph, origin='prometheus', kind='alert')
    alert_ids = [alert[0] for alert in alerts]

    dist_matrix = calculate_dist_matrix(nx_graph, alert_ids)
    draw_heatmap(dist_matrix, name='dist_matrix')

    alerts_ts = build_alerts_ts_lookup(alerts)
    corr_matrix = calculate_corr_matrix(alerts_ts)
    draw_heatmap(corr_matrix, name='corr_matrix')

    deps_matrix = calculate_deps_matrix(dist_matrix, corr_matrix)
    draw_heatmap(deps_matrix, name='deps_matrix')

    fault_view = build_fault_view(deps_matrix)
    draw_fault_view(fault_view)

    from_source = None
    # from_source = 'prometheus-alert-istiorequestdurationhigh-service-d-isotope'
    # from_source = 'prometheus-alert-istiorequestdurationhigh-service-svc-0-0-isotope'
    trajectories = find_fault_trajectories(fault_view, from_source=from_source)

    scored_trajectories = score_fault_trajectories(fault_view, trajectories)
    ranked_trajectories = rank_fault_trajectories(scored_trajectories)

    draw_trajectories(ranked_trajectories)

    print(ranked_trajectories)


def get_dep_graph(time_point):
    nodes = dep_graph.get_nodes(time_point=time_point)
    links = dep_graph.get_links(time_point=time_point)
    return nodes, links


def build_nx_graph(nodes, links):
    nx_graph = nx.DiGraph()
    for node in nodes:
        nx_graph.add_node(node.id, origin=node.origin, kind=node.kind, properties=node.properties)
    for link in links:
        nx_graph.add_edge(link.source.id, link.target.id)
    return nx_graph


def filter_graph_nodes(nx_graph, **filters):
    nodes = []
    for node in nx_graph.nodes(data=True):
        _node_id, node_data = node
        if all([node_data.get(key) == value for key, value in filters.items()]):
            nodes.append(node)
    return nodes


def calculate_dist_matrix(nx_graph, alert_ids):
    path_lengths = dict(nx.nx.all_pairs_shortest_path_length(nx_graph, cutoff=5))
    dist = {}
    for source_id in alert_ids:
        dist[source_id] = {}
        source_component = list(nx_graph[source_id])[0]
        for target_id in alert_ids:
            target_component = list(nx_graph[target_id])[0]
            path_length = path_lengths[source_component].get(target_component)
            if not path_length:
                dist_value = 0
            elif path_length == 1:
                dist_value = 1
            else:
                path_length -= 1
                dist_value = math.pow(2, -path_length)
            dist[source_id][target_id] = dist_value
    return pd.DataFrame(dist)


def calculate_corr_matrix(ts_data, corr_threshold=0.0):
    cols = ts_data.keys()
    df = pd.DataFrame(ts_data, columns=cols)
    corr_matrix = df.corr(method='pearson')
    indexes = list(corr_matrix.index)
    for ix in indexes:
        for iy in indexes:
            corr_val = corr_matrix.at[ix, iy]
            if abs(corr_val) < corr_threshold:
                corr_matrix.at[ix, iy] = 0
    return corr_matrix


def build_alerts_ts_lookup(alerts):
    alerts_ts = {}
    max_sample_len = -1
    for alert_id, alert_data in alerts:
        ts = get_alert_ts(alert_data)
        if not ts:
            continue
        _indexes, values = ts
        max_sample_len = max(max_sample_len, len(values))
        alerts_ts[alert_id] = values
    for alert_id in alerts_ts:
        values = alerts_ts[alert_id]
        last_val = values[-1]
        sample_len = len(values)
        alerts_ts[alert_id].extend([last_val] * (max_sample_len - sample_len))
    return alerts_ts


def get_alert_ts(alert):
    properties = alert['properties']
    labels = properties['labels']
    annotations = properties['annotations']
    query = annotations.get('query')
    if not query:
        return
    return get_ts(query, labels)


def get_ts(query, labels):
    results = prom_client.range_query(
        query, start, end, sampling)['data']['result']
    for result in results:
        metric_labels = result['metric']
        metric_values = result['values']
        if all(label in labels.items() for label in metric_labels.items()):
            return normalize_ts_values(metric_values)


def normalize_ts_values(raw_values):
    timestamps = []
    values = []
    for raw_value in raw_values:
        timestamps.append(int(raw_value[0]))
        values.append(float(raw_value[1]))
    t0 = timestamps[0]
    indexes = [int((t - t0) / sampling) for t in timestamps]
    return indexes, values


def calculate_deps_matrix(dist_matrix, corr_matrix):
    deps = {}
    indexes = list(corr_matrix.index)
    for ix in indexes:
        deps[ix] = {}
        for iy in indexes:
            dist_val = dist_matrix.at[ix, iy]
            corr_val = corr_matrix.at[ix, iy]
            dep_val = dist_val * corr_val
            deps[ix][iy] = abs(dep_val)
    return pd.DataFrame(deps)


def build_fault_view(deps_matrix, dep_threshold=0.1):
    fault_view = nx.DiGraph()
    alert_ids = list(deps_matrix.index)
    for alert_id in alert_ids:
        fault_view.add_node(alert_id)
    for source_id in alert_ids:
        for target_id in alert_ids:
            if source_id == target_id:
                continue
            dep_val = deps_matrix.at[source_id, target_id]
            if abs(dep_val) > dep_threshold:
                fault_view.add_edge(source_id, target_id, dep=dep_val)
    return fault_view


def draw_fault_view(fault_view):
    graph_viz = graphviz.Digraph(format='png', engine='sfdp')

    graph_viz.attr(label='Fault View', fontsize='16', fontcolor='black')
    graph_viz.attr('node', margin='0.2', style='filled', fillcolor='red', fontcolor='white')
    graph_viz.attr('edge', fontcolor='black', arrowhead='normal', arrowsize='2')

    for alert_id in fault_view.nodes:
        graph_viz.node(alert_id)

    for source_id, target_id in fault_view.edges:
        dep_val = "%.2f" % fault_view[source_id][target_id]['dep']
        graph_viz.edge(source_id, target_id, label=str(dep_val))

    graph_viz.render('fault_view')
    # graph_viz.view()


def find_fault_trajectories(fault_view, from_source=None):
    root_alerts = [node for node, outdegree in fault_view.out_degree(fault_view.nodes) if outdegree == 0]
    if from_source:
        source_alerts = [from_source]
    else:
        source_alerts = [node for node, indegree in fault_view.in_degree(fault_view.nodes) if indegree == 0]
    trajectories = []
    for source in source_alerts:
        for root in root_alerts:
            paths = [path for path in nx.all_simple_paths(fault_view, source=source, target=root)]
            trajectories.extend(paths)
    return trajectories


def score_fault_trajectories(fault_view, trajectories):
    scores = []
    for trajectory in trajectories:
        score = (trajectory, calculate_avg_dep(fault_view, trajectory))
        scores.append(score)
    return scores


def rank_fault_trajectories(trajectories):
    return sorted(trajectories, key=lambda x: x[1], reverse=True)


def calculate_avg_dep(fault_view, trajectory):
    sum_dep = 0
    for i in range(len(trajectory) - 1):
        sum_dep += fault_view[trajectory[i]][trajectory[i + 1]]['dep']
    return sum_dep / len(trajectory)


def draw_trajectories(ranked_trajectories):
    graph_viz = graphviz.Digraph(format='png')

    graph_viz.attr(label='Fault Trajectories', fontsize='16', fontcolor='black')
    graph_viz.attr('node', margin='0.2', style='filled', fillcolor='red', fontcolor='white')
    graph_viz.attr('edge', fontcolor='black', arrowhead='normal', arrowsize='2')

    for tid, ranked_trajectory in enumerate(ranked_trajectories):
        trajectory, score = ranked_trajectory
        prefixed_trajectory = ["t%i/%s" % (tid, node) for node in trajectory]
        subgraph_name = "cluster_%i" % tid
        with graph_viz.subgraph(name=subgraph_name) as t:
            t.attr(label='Fault trajectory #%i (score: %f)' % (tid, score))
            for node in prefixed_trajectory:
                t.node(node)
            for i in range(len(prefixed_trajectory) - 1):
                t.edge(prefixed_trajectory[i], prefixed_trajectory[i + 1])

    graph_viz.render('fault_trajectories')
    # graph_viz.view()


def draw_heatmap(data, name):
    sb.heatmap(data, annot=True, vmax=1.0, vmin=-1.0, cmap='RdYlGn_r', linewidths=0.3,
        xticklabels=True, yticklabels=True)
    plt.savefig(name, bbox_inches='tight', dpi=300)
    plt.clf()


if __name__ == '__main__':
    main()
