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

import abc

from orca.common import str_utils
from orca.graph import graph
from orca.topology import extractor


class Extractor(extractor.Extractor):

    """Base class for Kubernetes extractors."""

    @property
    def origin(self):
        return 'kubernetes'

    def extract(self, entity):
        node_id = self._extract_id(entity)
        properties = self._extract_properties(entity)
        return graph.Node(node_id, properties, self.origin, self.kind)

    def _extract_id(self, entity):
        return entity.metadata.uid

    @abc.abstractmethod
    def _extract_properties(self, entity):
        """Extracts properties from given K8S object."""


class PodExtractor(Extractor):

    """Extractor for Pod entities."""

    @property
    def kind(self):
        return 'pod'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        if entity.metadata.labels:
            properties['labels'] = entity.metadata.labels.copy()
        properties['ip'] = entity.status.pod_ip
        properties['node'] = entity.spec.node_name
        properties['containers'] = self._extract_containers(entity)
        properties['volumes'] = self._extract_volumes(entity)
        return properties

    def _extract_containers(self, entity):
        containers = []
        for container in entity.spec.containers:
            properties = {}
            properties['name'] = container.name
            properties['image'] = container.image
            properties['command'] = None
            if container.command:
                properties['command'] = str_utils.escape(" ".join(container.command))
            properties['env'] = self._extract_env(container)
            properties['env_from'] = None
            if container.env_from:
                properties['env_from'] = [env.to_dict() for env in container.env_from]
            containers.append(properties)
        return containers

    def _extract_env(self, container):
        if not container.env:
            return None
        env_vars = []
        for env in container.env:
            properties = {}
            properties['value_from'] = None
            if env.value_from:
                properties['value_from'] = env.value_from.to_dict()
            env_vars.append(properties)
        return env_vars

    def _extract_volumes(self, entity):
        volumes = []
        for volume in entity.spec.volumes:
            properties = {}
            properties['name'] = volume.name
            properties['secret'] = None
            if volume.secret:
                properties['secret'] = volume.secret.to_dict()
            properties['config_map'] = None
            if volume.config_map:
                properties['config_map'] = volume.config_map.to_dict()
            if volume.persistent_volume_claim:
                properties['persistent_volume_claim'] = volume.persistent_volume_claim.to_dict()
            volumes.append(properties)
        return volumes


class ServiceExtractor(Extractor):

    """Extractor for Service entities."""

    @property
    def kind(self):
        return 'service'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['type'] = entity.spec.type
        properties['ip'] = entity.spec.cluster_ip
        if entity.spec.selector:
            properties['selector'] = entity.spec.selector.copy()
        else:
            properties['selector'] = {}
        return properties


class EndpointsExtractor(Extractor):

    """Extractor for Endpoint entities."""

    @property
    def kind(self):
        return 'endpoints'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class DeploymentExtractor(Extractor):

    """Extractor for Deployment entities."""

    @property
    def kind(self):
        return 'deployment'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class ReplicaSetExtractor(Extractor):

    """Extractor for Replica Set entities."""

    @property
    def kind(self):
        return 'replica_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class DaemonSetExtractor(Extractor):

    """Extractor for Daemon Set entities."""

    @property
    def kind(self):
        return 'daemon_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class StatefulSetExtractor(Extractor):

    """Extractor for Stateful Set entities."""

    @property
    def kind(self):
        return 'stateful_set'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['labels'] = entity.metadata.labels.copy()
        properties['replicas'] = entity.spec.replicas
        properties['selector'] = entity.spec.selector.match_labels
        return properties


class ConfigMapExtractor(Extractor):

    """Extractor for Config Map entities."""

    @property
    def kind(self):
        return 'config_map'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class SecretExtractor(Extractor):

    """Extractor for Secret entities."""

    @property
    def kind(self):
        return 'secret'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class StorageClassExtractor(Extractor):

    """Extractor for Storage Class entities."""

    @property
    def kind(self):
        return 'storage_class'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['provisioner'] = entity.provisioner
        properties['reclaim_policy'] = entity.reclaim_policy
        properties['parameters'] = entity.parameters.copy()
        return properties


class PersistentVolumeExtractor(Extractor):

    """Extractor for Persistent Volume entities."""

    @property
    def kind(self):
        return 'persistent_volume'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['storage_class'] = entity.spec.storage_class_name
        if entity.spec.nfs:
            properties['nfs'] = self._extract_nfs(entity.spec.nfs)
        properties['host_path'] = entity.spec.host_path
        properties['capacity'] = None
        if entity.spec.capacity:
            properties['capacity'] = entity.spec.capacity.copy()
        return properties

    def _extract_nfs(self, nfs):
        nfs_properties = {}
        nfs_properties['path'] = nfs.path
        nfs_properties['read_only'] = nfs.read_only
        nfs_properties['server'] = nfs.server
        return nfs_properties


class PersistentVolumeClaimExtractor(Extractor):

    """Extractor for Persistent Volume Claim entities."""

    @property
    def kind(self):
        return 'persistent_volume_claim'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['storage_class'] = entity.spec.storage_class_name
        properties['volume_name'] = entity.spec.volume_name
        return properties


class HorizontalPodAutoscalerExtractor(Extractor):

    """Extractor for Horizontal Pod Autoscaler entities."""

    @property
    def kind(self):
        return 'horizontal_pod_autoscaler'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        properties['min_replicas'] = entity.spec.min_replicas
        properties['max_replicas'] = entity.spec.max_replicas
        properties['target_ref'] = self._extract_target_ref(entity.spec.scale_target_ref)
        return properties

    def _extract_target_ref(self, target_ref):
        return {'kind': target_ref.kind.lower(), 'name': target_ref.name}


class NodeExtractor(Extractor):

    """Extractor for Node entities."""

    @property
    def kind(self):
        return 'node'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        return properties


class NamespaceExtractor(Extractor):

    """Extractor for Namespace entities."""

    @property
    def kind(self):
        return 'namespace'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['labels'] = None
        if entity.metadata.labels:
            properties['labels'] = entity.metadata.labels.copy()
        properties['phase'] = entity.status.phase
        return properties
