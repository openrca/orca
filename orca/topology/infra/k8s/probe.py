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


class PodPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('pod')),
            extractor=extractor.PodExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class ServicePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('service')),
            extractor=extractor.ServiceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class EndpointsPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('endpoints')),
            extractor=extractor.EndpointsExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class DeploymentPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('deployment')),
            extractor=extractor.DeploymentExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class ReplicaSetPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('replica_set')),
            extractor=extractor.ReplicaSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class DaemonSetPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('daemon_set')),
            extractor=extractor.DaemonSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class StatefulSetPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('stateful_set')),
            extractor=extractor.StatefulSetExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class ConfigMapPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('config_map')),
            extractor=extractor.ConfigMapExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class SecretPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('secret')),
            extractor=extractor.SecretExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class StorageClassPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('storage_class')),
            extractor=extractor.StorageClassExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class PersistentVolumePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('persistent_volume')),
            extractor=extractor.PersistentVolumeExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class PersistentVolumeClaimPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('persistent_volume_claim')),
            extractor=extractor.PersistentVolumeClaimExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class HorizontalPodAutoscalerPullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('horizontal_pod_autoscaler')),
            extractor=extractor.HorizontalPodAutoscalerExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class NodePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('node')),
            extractor=extractor.NodeExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class NamespacePullProbe(probe.PullProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('namespace')),
            extractor=extractor.NamespaceExtractor(),
            synchronizer=utils.NodeSynchronizer(graph, create=False),
            resync_period=CONFIG.kubernetes.resync_period)


class PodPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('pod')),
            extractor=extractor.PodExtractor())


class ServicePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('service')),
            extractor=extractor.ServiceExtractor())


class EndpointsPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('endpoints')),
            extractor=extractor.EndpointsExtractor())


class DeploymentPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('deployment')),
            extractor=extractor.DeploymentExtractor())


class ReplicaSetPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('replica_set')),
            extractor=extractor.ReplicaSetExtractor())


class DaemonSetPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('daemon_set')),
            extractor=extractor.DaemonSetExtractor())


class StatefulSetPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('stateful_set')),
            extractor=extractor.StatefulSetExtractor())


class ConfigMapPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('config_map')),
            extractor=extractor.ConfigMapExtractor())


class SecretPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('secret')),
            extractor=extractor.SecretExtractor())


class StorageClassPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('storage_class')),
            extractor=extractor.StorageClassExtractor())


class PersistentVolumePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('persistent_volume')),
            extractor=extractor.PersistentVolumeExtractor())


class PersistentVolumeClaimPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('persistent_volume_claim')),
            extractor=extractor.PersistentVolumeClaimExtractor())


class HorizontalPodAutoscalerPushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('horizontal_pod_autoscaler')),
            extractor=extractor.HorizontalPodAutoscalerExtractor())


class NodePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('node')),
            extractor=extractor.NodeExtractor())


class NamespacePushProbe(probe.PushProbe):

    @classmethod
    def get(cls, graph):
        return cls(
            graph=graph,
            upstream_proxy=upstream.UpstreamProxy(
                client=k8s.ResourceProxyFactory.get('namespace')),
            extractor=extractor.NodeExtractor())
