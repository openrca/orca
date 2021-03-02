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

from orca.topology import linker, utils
from orca.topology.infra.k8s import matcher


class Linker(linker.Linker):

    """Base class for Kubernetes linkers."""


class ServiceToPodLinker(Linker):

    """Links Service entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.ServiceToPodMatcher())


class ReplicaSetToPodLinker(Linker):

    """Links Replica Set entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.ReplicaSetToPodMatcher())


class StatefulSetToPodLinker(Linker):

    """Links Stateful Set entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.StatefulSetToPodMatcher())


class DaemonSetToPodLinker(Linker):

    """Links Daemon Set entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='daemon_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.DaemonSetToPodMatcher())


class PodToNodeLinker(Linker):

    """Links Pod entities to Node entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            matcher=matcher.PodToNodeMatcher())


class ServiceToEndpointsLinker(Linker):

    """Links Serivce entities to Endpoint entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='endpoints'),
            matcher=matcher.ServiceToEndpointsMatcher())


class HorizontalPodAutoscalerToDeploymentLinker(Linker):

    """Links Horizontal Pod Autoscaler entities to Deployment entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class DeploymentToReplicaSetLinker(Linker):

    """Links Deployment entities to Replica Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            matcher=matcher.DeploymentToReplicaSetMatcher())


class HorizontalPodAutoscalerToReplicaSetLinker(Linker):

    """Links Horizontal Pod Autoscaler entities to Replica Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class HorizontalPodAutoscalerToStatefulSetLinker(Linker):

    """Links Horizontal Pod Autoscaler entities to Stateful Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class PodToConfigMapLinker(Linker):

    """Links Pod entities to Config Map entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='config_map'),
            matcher=matcher.PodToConfigMapMatcher())


class PodToSecretLinker(Linker):

    """Links Pod entities to Secret entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='secret'),
            matcher=matcher.PodToSecretMatcher())


class PersistentVolumeToStorageClassLinker(Linker):

    """Links Persistent Volume entities to Storage Class entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='storage_class'),
            matcher=matcher.PersistentVolumeToStorageClassMatcher())


class PersistentVolumeClaimToPersistentVolumeLinker(Linker):

    """Links Persistent Volume Claim entities to Persistent Volume entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            matcher=matcher.PersistentVolumeClaimToPersistentVolumeMatcher())


class PodToPersistentVolumeClaimLinker(Linker):

    """Links Pod entities to Persistent Volume Claim entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            matcher=matcher.PodToPersistentVolumeClaimMatcher())


class ClusterToNodeLinker(Linker):

    """Links Node entitites."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='cluster'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            matcher=matcher.ClusterToNodeMatcher())


class IngressToServiceLinker(Linker):

    """Links Ingress entities to Service entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='ingress'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.IngressToServiceMatcher())


class JobToPodLinker(Linker):

    """Links Job entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='job'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.JobToPodMatcher())


class CronJobToJobLinker(Linker):

    """Links CronJob entities to Job entities."""
    
    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='cron_job'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='job'),
            matcher=matcher.CronJobToJobMatcher())

