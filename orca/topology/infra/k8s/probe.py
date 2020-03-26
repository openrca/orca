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

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(k8s.ResourceProxyFactory.get(kind)),
            extractor=extractor,
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class PushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph, kind, extractor):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(k8s.ResourceProxyFactory.get(kind)),
            extractor=extractor)


class PodPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'pod', extractor.PodExtractor())


class PodPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'pod', extractor.PodExtractor())


class ServicePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'service', extractor.ServiceExtractor())


class ServicePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'service', extractor.ServiceExtractor())


class EndpointsPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'endpoints', extractor.EndpointsExtractor())


class EndpointsPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'endpoints', extractor.EndpointsExtractor())


class DeploymentPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'deployment', extractor.DeploymentExtractor())


class DeploymentPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'deployment', extractor.DeploymentExtractor())


class ReplicaSetPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'replica_set', extractor.ReplicaSetExtractor())


class ReplicaSetPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'replica_set', extractor.ReplicaSetExtractor())


class DaemonSetPullProbe(PullProbe):
    @classmethod
    def get(cls, graph):
        return super().get(graph, 'daemon_set', extractor.DaemonSetExtractor())


class DaemonSetPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'daemon_set', extractor.DaemonSetExtractor())


class StatefulSetPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'stateful_set', extractor.StatefulSetExtractor())


class StatefulSetPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'stateful_set', extractor.StatefulSetExtractor())


class ConfigMapPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'config_map', extractor.ConfigMapExtractor())


class ConfigMapPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'config_map', extractor.ConfigMapExtractor())


class SecretPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'secret', extractor.SecretExtractor())


class SecretPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'secret', extractor.SecretExtractor())


class StorageClassPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'storage_class', extractor.StorageClassExtractor())


class StorageClassPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'storage_class', extractor.StorageClassExtractor())


class PersistentVolumePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'persistent_volume', extractor.PersistentVolumeExtractor())


class PersistentVolumePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'persistent_volume', extractor.PersistentVolumeExtractor())


class PersistentVolumeClaimPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'persistent_volume_claim', extractor.PersistentVolumeClaimExtractor())


class PersistentVolumeClaimPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'persistent_volume_claim', extractor.PersistentVolumeClaimExtractor())


class HorizontalPodAutoscalerPullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'horizontal_pod_autoscaler', extractor.HorizontalPodAutoscalerExtractor())


class HorizontalPodAutoscalerPushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(
            graph, 'horizontal_pod_autoscaler', extractor.HorizontalPodAutoscalerExtractor())


class NodePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'node', extractor.NodeExtractor())


class NodePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'node', extractor.NodeExtractor())


class NamespacePullProbe(PullProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'namespace', extractor.NamespaceExtractor())


class NamespacePushProbe(PushProbe):

    @classmethod
    def get(cls, graph):
        return super().get(graph, 'namespace', extractor.NamespaceExtractor())
