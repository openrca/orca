from orca.common.clients import k8s
from orca.topology import linker
from orca.topology.infra.k8s import (cluster, config_map, daemon_set,
                                     deployment, node, pod, probe, replica_set,
                                     secret, service, stateful_set)


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            kind='pod',
            extractor=pod.PodExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')),
        probe.Probe(
            kind='service',
            extractor=service.ServiceExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')),
        probe.Probe(
            kind='deployment',
            extractor=deployment.DeploymentExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')),
        probe.Probe(
            kind='replica_set',
            extractor=replica_set.ReplicaSetExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')),
        probe.Probe(
            kind='daemon_set',
            extractor=daemon_set.DaemonSetExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')),
        probe.Probe(
            kind='stateful_set',
            extractor=stateful_set.StatefulSetExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')),
        probe.Probe(
            kind='config_map',
            extractor=config_map.ConfigMapExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')),
        probe.Probe(
            kind='secret',
            extractor=secret.SecretExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')),
        probe.Probe(
            kind='node',
            extractor=node.NodeExtractor(),
            graph=graph,
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')),
        cluster.ClusterProbe(kind='cluster', graph=graph)]


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
