from orca.common.clients.k8s import client as k8s
from orca.topology import linker
from orca.topology.infra.k8s import (cluster, config_map, daemon_set,
                                     deployment, node, pod, probe, replica_set,
                                     secret, service, stateful_set)


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            graph=graph,
            extractor=pod.PodExtractor('kubernetes', 'pod'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')),
        probe.Probe(
            graph=graph,
            extractor=service.ServiceExtractor('kubernetes', 'service'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')),
        probe.Probe(
            graph=graph,
            extractor=deployment.DeploymentExtractor('kubernetes', 'deployment'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')),
        probe.Probe(
            graph=graph,
            extractor=replica_set.ReplicaSetExtractor('kubernetes', 'replica_set'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')),
        probe.Probe(
            graph=graph,
            extractor=daemon_set.DaemonSetExtractor('kubernetes', 'daemon_set'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')),
        probe.Probe(
            graph=graph,
            extractor=stateful_set.StatefulSetExtractor('kubernetes', 'stateful_set'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')),
        probe.Probe(
            graph=graph,
            extractor=config_map.ConfigMapExtractor('kubernetes', 'config_map'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')),
        probe.Probe(
            graph=graph,
            extractor=secret.SecretExtractor('kubernetes', 'secret'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')),
        probe.Probe(
            graph=graph,
            extractor=node.NodeExtractor('kubernetes', 'node'),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')),
        cluster.ClusterProbe(graph=graph)]


def initialize_linkers(graph):
    return [
        linker.Linker(
            kind_a='pod',
            kind_b='service',
            graph=graph,
            matcher=pod.PodToServiceMatcher()),
        linker.Linker(
            kind_a='pod',
            kind_b='replica_set',
            graph=graph,
            matcher=pod.PodToReplicaSetMatcher()),
        linker.Linker(
            kind_a='pod',
            kind_b='stateful_set',
            graph=graph,
            matcher=pod.PodToStatefulSetMatcher()),
        linker.Linker(
            kind_a='pod',
            kind_b='daemon_set',
            graph=graph,
            matcher=pod.PodToDaemonSetMatcher()),
        linker.Linker(
            kind_a='pod',
            kind_b='node',
            graph=graph,
            matcher=pod.PodToNodeMatcher()),
        linker.Linker(
            kind_a='replica_set',
            kind_b='deployment',
            graph=graph,
            matcher=replica_set.ReplicaSetToDeploymentMatcher()),
        linker.Linker(
            kind_a='config_map',
            kind_b='pod',
            graph=graph,
            matcher=config_map.ConfigMapToPodMatcher()),
        linker.Linker(
            kind_a='secret',
            kind_b='pod',
            graph=graph,
            matcher=secret.SecretToPodMatcher()),
        linker.Linker(
            kind_a='node',
            kind_b='cluster',
            graph=graph,
            matcher=node.NodeToClusterMatcher())]
