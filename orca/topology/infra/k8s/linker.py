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


class NamespacedLinker(Linker):

    """Scopes linked entities by namespace."""

    def _get_target_query(self, node):
        return self._get_namespace_query(node)

    def _get_source_query(self, node):
        return self._get_namespace_query(node)

    def _get_namespace_query(self, node):
        return {
            'properties': {
                'namespace': node.properties.namespace
            }
        }


class PodToServiceLinker(NamespacedLinker):

    """Links Pod entities to Service entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.PodToServiceMatcher())


class PodToReplicaSetLinker(NamespacedLinker):

    """Links Pod entities to Replica Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            matcher=matcher.PodToReplicaSetMatcher())


class PodToStatefulSetLinker(NamespacedLinker):

    """Links Pod entities to Stateful Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            matcher=matcher.PodToStatefulSetMatcher())


class PodToDaemonSetLinker(NamespacedLinker):

    """Links Pod entities to Daemon Set entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='daemon_set'),
            matcher=matcher.PodToDaemonSetMatcher())


class PodToNodeLinker(Linker):

    """Links Pod entities to Node entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            matcher=matcher.PodToNodeMatcher())


class EndpointsToServiceLinker(NamespacedLinker):

    """Links Endpoint entities to Service entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='endpoints'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='service'),
            matcher=matcher.EndpointsToServiceMatcher())


class DeploymentToHorizontalPodAutoscalerLinker(NamespacedLinker):

    """Links Deployment entities to Horizontal Pod Autoscaler entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class ReplicaSetToDeploymentLinker(NamespacedLinker):

    """Links Replica Set entities to Deployment entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='deployment'),
            matcher=matcher.ReplicaSetToDeploymentMatcher())


class ReplicaSetToHorizontalPodAutoscalerLinker(NamespacedLinker):

    """Links Replica Set entities to Horizontal Pod Autoscaler entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='replica_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class StatefulSetToHorizontalPodAutoscalerLinker(NamespacedLinker):

    """Links Stateful Set entities to Horizontal Pod Autoscaler entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='stateful_set'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='horizontal_pod_autoscaler'),
            matcher=matcher.HorizontalPodAutoscalerMatcher())


class ConfigMapToPodLinker(NamespacedLinker):

    """Links Config Map entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='config_map'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.ConfigMapToPodMatcher())


class SecretToPodLinker(NamespacedLinker):

    """Links Secret entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='secret'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.SecretToPodMatcher())


class PersistentVolumeToStorageClassLinker(Linker):

    """Links Persistent Volume entities to Storage Class entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='storage_class'),
            matcher=matcher.PersistentVolumeToStorageClassMatcher())


class PersistentVolumeToPersistentVolumeClaimLinker(Linker):

    """Links Persistent Volume entities to Persistent Volume Claim entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            matcher=matcher.PersistentVolumeToPersistentVolumeClaimMatcher())


class PersistentVolumeClaimToPodLinker(NamespacedLinker):

    """Links Persistent Volume Claim entities to Pod entities."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='persistent_volume_claim'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='pod'),
            matcher=matcher.PersistentVolumeClaimToPodMatcher())


class NodeToClusterLinker(Linker):

    """Links Node entitites."""

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            source_spec=utils.NodeSpec(origin='kubernetes', kind='node'),
            target_spec=utils.NodeSpec(origin='kubernetes', kind='cluster'),
            matcher=matcher.NodeToClusterMatcher())
