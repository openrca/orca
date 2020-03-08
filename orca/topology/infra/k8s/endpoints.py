from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class EndpointsExtractor(extractor.Extractor):

    def get_kind(self):
        return 'endpoints'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class EndpointsToServiceMatcher(linker.Matcher):

    def are_linked(self, endpoints, service):
        match_namespace = k8s_linker.match_namespace(endpoints, service)
        match_name = endpoints.properties.name == service.properties.name
        return match_namespace and match_name
