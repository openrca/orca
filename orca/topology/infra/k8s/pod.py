from orca.common import str_utils
from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class PodExtractor(extractor.Extractor):

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
