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

from orca.common import config
from orca.topology import utils
from orca.topology.infra.k8s import cluster, linker, probe

CONFIG = config.CONFIG


def initialize_probes(graph):
    return [
        probe.PodPullProbe.get(graph),
        probe.PodPushProbe.get(graph),
        probe.ServicePullProbe.get(graph),
        probe.ServicePushProbe.get(graph),
        probe.EndpointsPullProbe.get(graph),
        probe.EndpointsPushProbe.get(graph),
        probe.DeploymentPullProbe.get(graph),
        probe.DeploymentPushProbe.get(graph),
        probe.ReplicaSetPullProbe.get(graph),
        probe.ReplicaSetPushProbe.get(graph),
        probe.DaemonSetPullProbe.get(graph),
        probe.DaemonSetPushProbe.get(graph),
        probe.StatefulSetPullProbe.get(graph),
        probe.StatefulSetPushProbe.get(graph),
        probe.ConfigMapPullProbe.get(graph),
        probe.ConfigMapPushProbe.get(graph),
        probe.SecretPullProbe.get(graph),
        probe.SecretPushProbe.get(graph),
        probe.StorageClassPullProbe.get(graph),
        probe.StorageClassPushProbe.get(graph),
        probe.PersistentVolumePullProbe.get(graph),
        probe.PersistentVolumePushProbe.get(graph),
        probe.PersistentVolumeClaimPullProbe.get(graph),
        probe.PersistentVolumeClaimPushProbe.get(graph),
        probe.HorizontalPodAutoscalerPullProbe.get(graph),
        probe.HorizontalPodAutoscalerPushProbe.get(graph),
        probe.NodePullProbe.get(graph),
        probe.NodePushProbe.get(graph),
        probe.NamespacePullProbe.get(graph),
        probe.NamespacePushProbe.get(graph),
        cluster.ClusterProbe(graph=graph)
    ]


def initialize_linkers(graph):
    linkers = [
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=linker.PodToServiceMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            matcher=linker.PodToReplicaSetMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            matcher=linker.PodToStatefulSetMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='daemon_set'),
            matcher=linker.PodToDaemonSetMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            matcher=linker.PodToNodeMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='endpoints'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=linker.EndpointsToServiceMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            matcher=linker.ReplicaSetToDeploymentMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='config_map'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=linker.ConfigMapToPodMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='secret'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=linker.SecretToPodMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='storage_class'),
            matcher=linker.PersistentVolumeToStorageClassMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            matcher=linker.PersistentVolumeToPersistentVolumeClaimMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=linker.PersistentVolumeClaimToPodMatcher()
        ),
        linker.Linker(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='cluster'),
            matcher=linker.NodeToClusterMatcher()
        )
    ]

    for kind in ('deployment', 'replica_set', 'stateful_set'):
        linkers.append(
            linker.Linker(
                graph=graph,
                source_spec=utils.NodeSpec(origin='kubernetes', kind=kind),
                target_spec=utils.NodeSpec(origin='kubernetes', kind='horszontal_pod_autoscaler'),
                matcher=linker.HorizontalPodAutoscalerMatcher()
            ))

    for kind in ('pod', 'service', 'deployment', 'replica_set', 'daemon_set', 'stateful_set',
                 'config_map', 'secret', 'persistent_volume_claim', 'horizontal_pod_autoscaler'):
        linkers.append(
            linker.Linker(
                graph=graph,
                source_spec=utils.NodeSpec(origin='kubernetes', kind=kind),
                target_spec=utils.NodeSpec(origin='kubernetes', kind='namespace'),
                matcher=linker.NamespaceMatcher()
            ))

    return linkers
