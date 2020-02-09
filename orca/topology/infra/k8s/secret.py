from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class SecretExtractor(extractor.Extractor):

    def _extract_kind(self, entity):
        return 'secret'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class SecretToPodMatcher(linker.Matcher):

    def are_linked(self, secret, pod):
        match_namespace = k8s_linker.match_namespace(secret, pod)
        match_env = self._match_env(secret, pod)
        match_volume = self._match_volume(secret, pod)
        return match_namespace and (match_env or match_volume)

    def _match_env(self, secret, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if env_var.value_from and \
                       env_var.value_from.secret_key_ref and \
                       env_var.value_from.secret_key_ref.name == secret.properties.name:
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.secret_ref and \
                       env_from.secret_ref.name == secret.properties.name:
                        return True
        return False

    def _match_volume(self, secret, pod):
        for volume in pod.properties.volumes:
            if volume.secret and volume.secret.secret_name == secret.properties.name:
                return True
        return False
