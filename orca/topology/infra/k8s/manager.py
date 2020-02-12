from orca.common.clients.k8s import client as k8s
from orca.topology import linker
from orca.topology.infra.k8s import (cluster, config_map, daemon_set,
                                     deployment, node, pod, probe, replica_set,
                                     secret, service, stateful_set)


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            origin="kubernetes",
            kind='pod',
            graph=graph,
            extractor=pod.PodExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')),
        probe.Probe(
            origin="kubernetes",
            kind='service',
            graph=graph,
            extractor=service.ServiceExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')),
        probe.Probe(
            origin="kubernetes",
            kind='deployment',
            graph=graph,
            extractor=deployment.DeploymentExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')),
        probe.Probe(
            origin="kubernetes",
            kind='replica_set',
            graph=graph,
            extractor=replica_set.ReplicaSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')),
        probe.Probe(
            origin="kubernetes",
            kind='daemon_set',
            graph=graph,
            extractor=daemon_set.DaemonSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')),
        probe.Probe(
            origin="kubernetes",
            kind='stateful_set',
            graph=graph,
            extractor=stateful_set.StatefulSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')),
        probe.Probe(
            origin="kubernetes",
            kind='config_map',
            graph=graph,
            extractor=config_map.ConfigMapExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')),
        probe.Probe(
            origin="kubernetes",
            kind='secret',
            graph=graph,
            extractor=secret.SecretExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')),
        probe.Probe(
            origin="kubernetes",
            kind='node',
            graph=graph,
            extractor=node.NodeExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')),
        cluster.ClusterProbe(
            origin='kubernetes',
            kind='cluster',
            graph=graph)]


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
