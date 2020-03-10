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
from orca.topology import linker
from orca.topology.infra.k8s import (
    cluster, config_map, daemon_set, deployment, endpoints,
    horizontal_pod_autoscaler, namespace, node, persistent_volume,
    persistent_volume_claim, pod, probe, replica_set, secret, service,
    stateful_set, storage_class)


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            graph=graph,
            extractor=pod.PodExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')),
        probe.Probe(
            graph=graph,
            extractor=service.ServiceExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')),
        probe.Probe(
            graph=graph,
            extractor=endpoints.EndpointsExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'endpoints')),
        probe.Probe(
            graph=graph,
            extractor=deployment.DeploymentExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')),
        probe.Probe(
            graph=graph,
            extractor=replica_set.ReplicaSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')),
        probe.Probe(
            graph=graph,
            extractor=daemon_set.DaemonSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')),
        probe.Probe(
            graph=graph,
            extractor=stateful_set.StatefulSetExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')),
        probe.Probe(
            graph=graph,
            extractor=config_map.ConfigMapExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')),
        probe.Probe(
            graph=graph,
            extractor=secret.SecretExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')),
        probe.Probe(
            graph=graph,
            extractor=storage_class.StorageClassExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'storage_class')),
        probe.Probe(
            graph=graph,
            extractor=persistent_volume.PersistentVolumeExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume')),
        probe.Probe(
            graph=graph,
            extractor=persistent_volume_claim.PersistentVolumeClaimExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume_claim')),
        probe.Probe(
            graph=graph,
            extractor=node.NodeExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')),
        probe.Probe(
            graph=graph,
            extractor=namespace.NamespaceExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'namespace')),
        probe.Probe(
            graph=graph,
            extractor=horizontal_pod_autoscaler.HorizontalPodAutoscalerExtractor(),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'horizontal_pod_autoscaler')),
        cluster.ClusterProbe(graph=graph)]


def initialize_linkers(graph):
    linkers = [
        linker.Linker(
            source_kind='pod',
            target_kind='service',
            graph=graph,
            matcher=pod.PodToServiceMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='replica_set',
            graph=graph,
            matcher=pod.PodToReplicaSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='stateful_set',
            graph=graph,
            matcher=pod.PodToStatefulSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='daemon_set',
            graph=graph,
            matcher=pod.PodToDaemonSetMatcher()),
        linker.Linker(
            source_kind='pod',
            target_kind='node',
            graph=graph,
            matcher=pod.PodToNodeMatcher()),
        linker.Linker(
            source_kind='endpoints',
            target_kind='service',
            graph=graph,
            matcher=endpoints.EndpointsToServiceMatcher()),
        linker.Linker(
            source_kind='replica_set',
            target_kind='deployment',
            graph=graph,
            matcher=replica_set.ReplicaSetToDeploymentMatcher()),
        linker.Linker(
            source_kind='config_map',
            target_kind='pod',
            graph=graph,
            matcher=config_map.ConfigMapToPodMatcher()),
        linker.Linker(
            source_kind='secret',
            target_kind='pod',
            graph=graph,
            matcher=secret.SecretToPodMatcher()),
        linker.Linker(
            source_kind='persistent_volume',
            target_kind='storage_class',
            graph=graph,
            matcher=persistent_volume.PersistentVolumeToStorageClassMatcher()),
        linker.Linker(
            source_kind='persistent_volume',
            target_kind='persistent_volume_claim',
            graph=graph,
            matcher=persistent_volume.PersistentVolumeToPersistentVolumeClaimMatcher()),
        linker.Linker(
            source_kind='persistent_volume_claim',
            target_kind='pod',
            graph=graph,
            matcher=persistent_volume_claim.PersistentVolumeClaimToPodMatcher()),
        linker.Linker(
            source_kind='node',
            target_kind='cluster',
            graph=graph,
            matcher=node.NodeToClusterMatcher())]

    for kind in ('deployment', 'replica_set', 'stateful_set'):
        linkers.append(
            linker.Linker(
                source_kind=kind,
                target_kind='horizontal_pod_autoscaler',
                graph=graph,
                matcher=horizontal_pod_autoscaler.HorizontalPodAutoscalerMatcher()))

    for kind in ('pod', 'service', 'deployment', 'replica_set', 'daemon_set', 'stateful_set',
                 'config_map', 'secret', 'persistent_volume_claim', 'horizontal_pod_autoscaler'):
        linkers.append(
            linker.Linker(
                source_kind=kind,
                target_kind='namespace',
                graph=graph,
                matcher=namespace.NamespaceMatcher()))

    return linkers
