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

from orca.common import str_utils
from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class PodExtractor(extractor.Extractor):

    def get_kind(self):
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


class PodToServiceMatcher(linker.Matcher):

    def are_linked(self, pod, service):
        match_namespace = k8s_linker.match_namespace(pod, service)
        match_selector = k8s_linker.match_selector(pod, service.properties.selector)
        return match_namespace and match_selector


class PodToReplicaSetMatcher(linker.Matcher):

    def are_linked(self, pod, replica_set):
        match_namespace = k8s_linker.match_namespace(pod, replica_set)
        match_selector = k8s_linker.match_selector(pod, replica_set.properties.selector)
        return match_namespace and match_selector


class PodToStatefulSetMatcher(linker.Matcher):

    def are_linked(self, pod, stateful_set):
        match_namespace = k8s_linker.match_namespace(pod, stateful_set)
        match_selector = k8s_linker.match_selector(pod, stateful_set.properties.selector)
        return match_namespace and match_selector


class PodToDaemonSetMatcher(linker.Matcher):

    def are_linked(self, pod, daemon_set):
        match_namespace = k8s_linker.match_namespace(pod, daemon_set)
        match_selector = k8s_linker.match_selector(pod, daemon_set.properties.selector)
        return match_namespace and match_selector


class PodToNodeMatcher(linker.Matcher):

    def are_linked(self, pod, node):
        return pod.properties.node == node.properties.name
