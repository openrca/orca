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
from orca.topology import utils
from orca.topology.infra.k8s import cluster, extractor, linker, probe


def initialize_probes(graph):
    k8s_client = k8s.ClientFactory.get()
    return [
        probe.Probe(
            graph=graph,
            extractor=extractor.PodExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'pod')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.ServiceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'service')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.EndpointsExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'endpoints')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.DeploymentExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'deployment')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.ReplicaSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'replica_set')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.DaemonSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'daemon_set')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.StatefulSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'stateful_set')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.ConfigMapExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'config_map')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.SecretExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'secret')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.StorageClassExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'storage_class')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.PersistentVolumeExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.PersistentVolumeClaimExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'persistent_volume_claim')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.HorizontalPodAutoscalerExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'horizontal_pod_autoscaler')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.NodeExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'node')
        ),
        probe.Probe(
            graph=graph,
            extractor=extractor.NamespaceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph),
            k8s_client=k8s.ResourceProxyFactory.get(k8s_client, 'namespace')
        ),
        cluster.ClusterProbe(
            graph=graph
        )
    ]


def initialize_linkers(graph):
    linkers = [
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            graph=graph,
            matcher=linker.PodToServiceMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            graph=graph,
            matcher=linker.PodToReplicaSetMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            graph=graph,
            matcher=linker.PodToStatefulSetMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='daemon_set'),
            graph=graph,
            matcher=linker.PodToDaemonSetMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            graph=graph,
            matcher=linker.PodToNodeMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='endpoints'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            graph=graph,
            matcher=linker.EndpointsToServiceMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            graph=graph,
            matcher=linker.ReplicaSetToDeploymentMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='config_map'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            graph=graph,
            matcher=linker.ConfigMapToPodMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='secret'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            graph=graph,
            matcher=linker.SecretToPodMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='storage_class'),
            graph=graph,
            matcher=linker.PersistentVolumeToStorageClassMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            graph=graph,
            matcher=linker.PersistentVolumeToPersistentVolumeClaimMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            graph=graph,
            matcher=linker.PersistentVolumeClaimToPodMatcher()
        ),
        linker.Linker(
            source_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='cluster'),
            graph=graph,
            matcher=linker.NodeToClusterMatcher()
        )
    ]

    for kind in ('deployment', 'replica_set', 'stateful_set'):
        linkers.append(
            linker.Linker(
                source_spec=utils.NodeSpec(origin='kubernetes', kind=kind),
                target_spec=utils.NodeSpec(origin='kubernetes', kind='horszontal_pod_autoscaler'),
                graph=graph,
                matcher=linker.HorizontalPodAutoscalerMatcher()
            ))

    for kind in ('pod', 'service', 'deployment', 'replica_set', 'daemon_set', 'stateful_set',
                 'config_map', 'secret', 'persistent_volume_claim', 'horizontal_pod_autoscaler'):
        linkers.append(
            linker.Linker(
                source_spec=utils.NodeSpec(origin='kubernetes', kind=kind),
                target_spec=utils.NodeSpec(origin='kubernetes', kind='namespace'),
                graph=graph,
                matcher=linker.NamespaceMatcher()
            ))

    return linkers
