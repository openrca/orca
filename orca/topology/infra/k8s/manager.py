# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orca.common.clients.k8s import client as k8s
from orca.topology import synchronizer
from orca.topology.infra.k8s import cluster, extractor, linker, probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            graph=graph,
            extractor=extractor.PodExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')),
        probe.Probe(
            graph=graph,
            extractor=extractor.ServiceExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')),
        probe.Probe(
            graph=graph,
            extractor=extractor.EndpointsExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'endpoints')),
        probe.Probe(
            graph=graph,
            extractor=extractor.DeploymentExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')),
        probe.Probe(
            graph=graph,
            extractor=extractor.ReplicaSetExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')),
        probe.Probe(
            graph=graph,
            extractor=extractor.DaemonSetExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')),
        probe.Probe(
            graph=graph,
            extractor=extractor.StatefulSetExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')),
        probe.Probe(
            graph=graph,
            extractor=extractor.ConfigMapExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')),
        probe.Probe(
            graph=graph,
            extractor=extractor.SecretExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')),
        probe.Probe(
            graph=graph,
            extractor=extractor.StorageClassExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'storage_class')),
        probe.Probe(
            graph=graph,
            extractor=extractor.PersistentVolumeExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume')),
        probe.Probe(
            graph=graph,
            extractor=extractor.PersistentVolumeClaimExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume_claim')),
        probe.Probe(
            graph=graph,
            extractor=extractor.HorizontalPodAutoscalerExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'horizontal_pod_autoscaler')),
        probe.Probe(
            graph=graph,
            extractor=extractor.NodeExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')),
        probe.Probe(
            graph=graph,
            extractor=extractor.NamespaceExtractor(),
            synchronizer=synchronizer.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'namespace')),
        cluster.ClusterProbe(graph=graph)]


def initialize_linkers(graph):
    linkers = [
        linker.Linker(
            source_kind='pod',
            target_kind='service',
            graph=graph,
            matcher=linker.PodToServiceMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='replica_set',
            graph=graph,
            matcher=linker.PodToReplicaSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='stateful_set',
            graph=graph,
            matcher=linker.PodToStatefulSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='daemon_set',
            graph=graph,
            matcher=linker.PodToDaemonSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='node',
            graph=graph,
            matcher=linker.PodToNodeMatcher()),
        linker.Linker(
            source_kind='endpoints',
            target_kind='service',
            graph=graph,
            matcher=linker.EndpointsToServiceMatcher()),
        linker.Linker(
            source_kind='replica_set',
            target_kind='deployment',
            graph=graph,
            matcher=linker.ReplicaSetToDeploymentMatcher()),
        linker.Linker(
            source_kind='config_map',
            target_kind='pod',
            graph=graph,
            matcher=linker.ConfigMapToPodMatcher()),
        linker.Linker(
            source_kind='secret',
            target_kind='pod',
            graph=graph,
            matcher=linker.SecretToPodMatcher()),
        linker.Linker(
            source_kind='persistent_volume',
            target_kind='storage_class',
            graph=graph,
            matcher=linker.PersistentVolumeToStorageClassMatcher()),
        linker.Linker(
            source_kind='persistent_volume',
            target_kind='persistent_volume_claim',
            graph=graph,
            matcher=linker.PersistentVolumeToPersistentVolumeClaimMatcher()),
        linker.Linker(
            source_kind='persistent_volume_claim',
            target_kind='pod',
            graph=graph,
            matcher=linker.PersistentVolumeClaimToPodMatcher()),
        linker.Linker(
            source_kind='node',
            target_kind='cluster',
            graph=graph,
            matcher=linker.NodeToClusterMatcher())]

    for kind in ('deployment', 'replica_set', 'stateful_set'):
        linkers.append(
            linker.Linker(
                source_kind=kind,
                target_kind='horizontal_pod_autoscaler',
                graph=graph,
                matcher=linker.HorizontalPodAutoscalerMatcher()))

    for kind in ('pod', 'service', 'deployment', 'replica_set', 'daemon_set', 'stateful_set',
                 'config_map', 'secret', 'persistent_volume_claim', 'horizontal_pod_autoscaler'):
        linkers.append(
            linker.Linker(
                source_kind=kind,
                target_kind='namespace',
                graph=graph,
                matcher=linker.NamespaceMatcher()))

    return linkers
