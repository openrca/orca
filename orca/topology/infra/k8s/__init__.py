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

from orca.topology import bundle
from orca.topology.infra.istio import linker as istio_linker
from orca.topology.infra.k8s import cluster, linker, probe


def get_probes():
    return [
        bundle.ProbeBundle(
            probe=probe.PodPullProbe,
            linkers=[
                linker.ServiceToPodLinker,
                linker.ReplicaSetToPodLinker,
                linker.StatefulSetToPodLinker,
                linker.DaemonSetToPodLinker,
                linker.PodToNodeLinker,
                linker.PodToConfigMapLinker,
                linker.PodToSecretLinker,
                linker.PodToPersistentVolumeClaimLinker,
                linker.JobToPodLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.PodPushProbe,
            linkers=[
                linker.ServiceToPodLinker,
                linker.ReplicaSetToPodLinker,
                linker.StatefulSetToPodLinker,
                linker.DaemonSetToPodLinker,
                linker.PodToNodeLinker,
                linker.PodToConfigMapLinker,
                linker.PodToSecretLinker,
                linker.PodToPersistentVolumeClaimLinker,
                linker.JobToPodLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.ServicePullProbe,
            linkers=[
                linker.ServiceToPodLinker,
                linker.ServiceToEndpointsLinker,
                istio_linker.ServiceToVirtualServiceLinker,
                istio_linker.ServiceToDestinationRuleLinker,
                linker.IngressToServiceLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.ServicePushProbe,
            linkers=[
                linker.ServiceToPodLinker,
                linker.ServiceToEndpointsLinker,
                istio_linker.ServiceToVirtualServiceLinker,
                istio_linker.ServiceToDestinationRuleLinker,
                linker.IngressToServiceLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.EndpointsPullProbe, linkers=[linker.ServiceToEndpointsLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.EndpointsPushProbe, linkers=[linker.ServiceToEndpointsLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.DeploymentPullProbe,
            linkers=[
                linker.HorizontalPodAutoscalerToDeploymentLinker,
                linker.DeploymentToReplicaSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.DeploymentPushProbe,
            linkers=[
                linker.HorizontalPodAutoscalerToDeploymentLinker,
                linker.DeploymentToReplicaSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.ReplicaSetPullProbe,
            linkers=[
                linker.ReplicaSetToPodLinker,
                linker.DeploymentToReplicaSetLinker,
                linker.HorizontalPodAutoscalerToReplicaSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.ReplicaSetPushProbe,
            linkers=[
                linker.ReplicaSetToPodLinker,
                linker.DeploymentToReplicaSetLinker,
                linker.HorizontalPodAutoscalerToReplicaSetLinker,
            ],
        ),
        bundle.ProbeBundle(probe=probe.DaemonSetPullProbe, linkers=[linker.DaemonSetToPodLinker]),
        bundle.ProbeBundle(probe=probe.DaemonSetPushProbe, linkers=[linker.DaemonSetToPodLinker]),
        bundle.ProbeBundle(
            probe=probe.StatefulSetPullProbe,
            linkers=[
                linker.StatefulSetToPodLinker,
                linker.HorizontalPodAutoscalerToStatefulSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.StatefulSetPushProbe,
            linkers=[
                linker.StatefulSetToPodLinker,
                linker.HorizontalPodAutoscalerToStatefulSetLinker,
            ],
        ),
        bundle.ProbeBundle(probe=probe.ConfigMapPullProbe, linkers=[linker.PodToConfigMapLinker]),
        bundle.ProbeBundle(probe=probe.ConfigMapPushProbe, linkers=[linker.PodToConfigMapLinker]),
        bundle.ProbeBundle(probe=probe.SecretPullProbe, linkers=[linker.PodToSecretLinker]),
        bundle.ProbeBundle(probe=probe.SecretPushProbe, linkers=[linker.PodToSecretLinker]),
        bundle.ProbeBundle(
            probe=probe.StorageClassPullProbe, linkers=[linker.PersistentVolumeToStorageClassLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.StorageClassPushProbe, linkers=[linker.PersistentVolumeToStorageClassLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.PersistentVolumePullProbe,
            linkers=[
                linker.PersistentVolumeToStorageClassLinker,
                linker.PersistentVolumeClaimToPersistentVolumeLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.PersistentVolumePushProbe,
            linkers=[
                linker.PersistentVolumeToStorageClassLinker,
                linker.PersistentVolumeClaimToPersistentVolumeLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.PersistentVolumeClaimPullProbe,
            linkers=[
                linker.PersistentVolumeClaimToPersistentVolumeLinker,
                linker.PodToPersistentVolumeClaimLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.PersistentVolumeClaimPushProbe,
            linkers=[
                linker.PersistentVolumeClaimToPersistentVolumeLinker,
                linker.PodToPersistentVolumeClaimLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.HorizontalPodAutoscalerPullProbe,
            linkers=[
                linker.HorizontalPodAutoscalerToDeploymentLinker,
                linker.HorizontalPodAutoscalerToReplicaSetLinker,
                linker.HorizontalPodAutoscalerToStatefulSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.HorizontalPodAutoscalerPushProbe,
            linkers=[
                linker.HorizontalPodAutoscalerToDeploymentLinker,
                linker.HorizontalPodAutoscalerToReplicaSetLinker,
                linker.HorizontalPodAutoscalerToStatefulSetLinker,
            ],
        ),
        bundle.ProbeBundle(
            probe=probe.NodePullProbe, linkers=[linker.PodToNodeLinker, linker.ClusterToNodeLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.NodePushProbe, linkers=[linker.PodToNodeLinker, linker.ClusterToNodeLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.JobPullProbe, linkers=[linker.JobToPodLinker, linker.CronJobToJobLinker]
        ),
        bundle.ProbeBundle(
            probe=probe.JobPushProbe, linkers=[linker.JobToPodLinker, linker.CronJobToJobLinker]
        ),
        bundle.ProbeBundle(probe=probe.IngressPullProbe, linkers=[linker.IngressToServiceLinker]),
        bundle.ProbeBundle(probe=probe.IngressPushProbe, linkers=[linker.IngressToServiceLinker]),
        bundle.ProbeBundle(probe=probe.CronJobPullProbe, linkers=[linker.CronJobToJobLinker]),
        bundle.ProbeBundle(probe=probe.CronJobPushProbe, linkers=[linker.CronJobToJobLinker]),
        bundle.ProbeBundle(probe=cluster.ClusterProbe, linkers=[linker.ClusterToNodeLinker]),
    ]
