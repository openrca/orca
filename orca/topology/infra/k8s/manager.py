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

from orca.topology.infra.k8s import cluster, linker, probe


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
    return [
        linker.PodToServiceLinker.get(graph),
        linker.PodToReplicaSetLinker.get(graph),
        linker.PodToStatefulSetLinker.get(graph),
        linker.PodToDaemonSetLinker.get(graph),
        linker.PodToNodeLinker.get(graph),
        linker.EndpointsToServiceLinker.get(graph),
        linker.DeploymentToHorizontalPodAutoscalerLinker.get(graph),
        linker.ReplicaSetToDeploymentLinker.get(graph),
        linker.ReplicaSetToHorizontalPodAutoscalerLinker.get(graph),
        linker.StatefulSetToHorizontalPodAutoscalerLinker.get(graph),
        linker.ConfigMapToPodLinker.get(graph),
        linker.SecretToPodLinker.get(graph),
        linker.PersistentVolumeToStorageClassLinker.get(graph),
        linker.PersistentVolumeToPersistentVolumeClaimLinker.get(graph),
        linker.PersistentVolumeClaimToPodLinker.get(graph),
        linker.NodeToClusterLinker.get(graph),
    ]
