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
from orca.common.clients.k8s import client as k8s
from orca.topology import probe, utils
from orca.topology.infra.k8s import extractor, upstream

CONFIG = config.CONFIG


class PullProbe(probe.PullProbe):

    """Base pull probe for Kubernetes."""

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(k8s.ResourceProxyFactory.get(kind)),
            extractor=extractor,
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.probes.kubernetes.resync_period)


class PushProbe(probe.PushProbe):

    """Base push probe for Kubernetes."""

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(k8s.ResourceProxyFactory.get(kind)),
            extractor=extractor)


class PodPullProbe(PullProbe):

    """Pod pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'pod', extractor.PodExtractor())


class PodPushProbe(PushProbe):

    """Pod push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'pod', extractor.PodExtractor())


class ServicePullProbe(PullProbe):

    """Service pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'service', extractor.ServiceExtractor())


class ServicePushProbe(PushProbe):

    """Service push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'service', extractor.ServiceExtractor())


class EndpointsPullProbe(PullProbe):

    """Endpoint pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'endpoints', extractor.EndpointsExtractor())


class EndpointsPushProbe(PushProbe):

    """Endpoint push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'endpoints', extractor.EndpointsExtractor())


class DeploymentPullProbe(PullProbe):

    """Deployment pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'deployment', extractor.DeploymentExtractor())


class DeploymentPushProbe(PushProbe):

    """Deployment push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'deployment', extractor.DeploymentExtractor())


class ReplicaSetPullProbe(PullProbe):

    """Replica Set pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'replica_set', extractor.ReplicaSetExtractor())


class ReplicaSetPushProbe(PushProbe):

    """Replica Set push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'replica_set', extractor.ReplicaSetExtractor())


class DaemonSetPullProbe(PullProbe):

    """Daemon Set pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'daemon_set', extractor.DaemonSetExtractor())


class DaemonSetPushProbe(PushProbe):

    """Daemon Set push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'daemon_set', extractor.DaemonSetExtractor())


class StatefulSetPullProbe(PullProbe):

    """Stateful Set pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'stateful_set', extractor.StatefulSetExtractor())


class StatefulSetPushProbe(PushProbe):

    """Stateful Set push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'stateful_set', extractor.StatefulSetExtractor())


class ConfigMapPullProbe(PullProbe):

    """Config Map pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'config_map', extractor.ConfigMapExtractor())


class ConfigMapPushProbe(PushProbe):

    """Config Map push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'config_map', extractor.ConfigMapExtractor())


class SecretPullProbe(PullProbe):

    """Secret pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'secret', extractor.SecretExtractor())


class SecretPushProbe(PushProbe):

    """Secret push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'secret', extractor.SecretExtractor())


class StorageClassPullProbe(PullProbe):

    """Storage Class pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'storage_class', extractor.StorageClassExtractor())


class StorageClassPushProbe(PushProbe):

    """Storage Class push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'storage_class', extractor.StorageClassExtractor())


class PersistentVolumePullProbe(PullProbe):

    """Persistent Volume pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'persistent_volume', extractor.PersistentVolumeExtractor())


class PersistentVolumePushProbe(PushProbe):

    """Persistent Volume push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'persistent_volume', extractor.PersistentVolumeExtractor())


class PersistentVolumeClaimPullProbe(PullProbe):

    """Persistent Volume Claim pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'persistent_volume_claim', extractor.PersistentVolumeClaimExtractor())


class PersistentVolumeClaimPushProbe(PushProbe):

    """Persistent Volume Claim push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'persistent_volume_claim', extractor.PersistentVolumeClaimExtractor())


class HorizontalPodAutoscalerPullProbe(PullProbe):

    """Horizontal Pod Autoscaler pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'horizontal_pod_autoscaler', extractor.HorizontalPodAutoscalerExtractor())


class HorizontalPodAutoscalerPushProbe(PushProbe):

    """Horizontal Pod Autoscaler push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'horizontal_pod_autoscaler', extractor.HorizontalPodAutoscalerExtractor())


class NodePullProbe(PullProbe):

    """Node pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'node', extractor.NodeExtractor())


class NodePushProbe(PushProbe):

    """Node push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'node', extractor.NodeExtractor())


class NamespacePullProbe(PullProbe):

    """Namespace pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'namespace', extractor.NamespaceExtractor())


class NamespacePushProbe(PushProbe):

    """Namespace push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'namespace', extractor.NamespaceExtractor())


class IngressPullProbe(PullProbe):

    """Ingress pull probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'ingress', extractor.IngressExtractor())


class IngressPushProbe(PushProbe):

    """Ingress push probe."""

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'ingress', extractor.IngressExtractor())
