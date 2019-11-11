import copy

import py2neo as graph_lib

from orca.graph.drivers import client
from orca import graph


class Neo4jClient(client.Client):

    """Neo4j Graph DB client."""

    def __init__(self, host, port, user=None, password=None):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = graph_lib.Graph(
                scheme='bolt',
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password)
        return self._client

    def get_nodes(self, metadata=None):
        if not metadata:
            metadata = {}
        lib_nodes = self.client.nodes.match(**metadata)
        return list(map(self._build_node_obj, lib_nodes))

    def get_node(self, id):
        lib_node = self._get_node(id)
        if lib_node:
            return self._build_node_obj(lib_node)

    def add_node(self, node):
        properties = copy.deepcopy(node.metadata)
        properties['_id'] = node.id
        properties['_kind'] = node.kind
        lib_node = graph_lib.Node(**properties)
        self.client.create(lib_node)

    def update_node(self, node):
        lib_node = self._get_node(node.id)
        lib_node.update(node.metadata)
        self.client.push(lib_node)

    def delete_node(self, node):
        lib_node = self._get_node(node.id)
        self.client.delete(lib_node)

    def get_links(self, metadata=None):
        if not metadata:
            metadata = {}
        rels = self.client.relationships.match(**metadata)
        return list(map(self._build_link_obj, rels))

    def get_link(self, id):
        rel = self._get_rel(id)
        if rel:
            return self._build_link_obj(rel)

    def add_link(self, link):
        properties = copy.deepcopy(link.metadata)
        properties['_id'] = link.id
        source_lib_node = self._get_node(link.source.id)
        target_lib_node = self._get_node(link.target.id)
        rel = graph_lib.Relationship(
            source_lib_node, target_lib_node, **properties)
        self.client.create(rel)

    def update_link(self, link):
        rel = self._get_rel(link.id)
        rel.update(link.metadata)
        self.client.push(rel)

    def delete_link(self, link):
        rel = self._get_rel(link.id)
        self.client.separate(rel)

    def get_node_links(self, node):
        lib_node = self._get_node(node.id)
        rels = self._get_node_rels(lib_node)
        return list(map(self._build_link_obj, rels))

    def _get_node(self, id):
        return self.client.nodes.match(_id=id).first()

    def _get_node_rels(self, lib_node):
        rels = self.client.relationships.match([lib_node])
        return list(rels)

    def _get_rel(self, id):
        return self.client.relationships.match(_id=id).first()

    def _build_node_obj(self, lib_node):
        properties = dict(lib_node)
        id = properties.pop('_id')
        kind = properties.pop('_kind')
        return graph.Node(id, properties, kind)

    def _build_link_obj(self, rel):
        properties = dict(rel)
        id = properties.pop('_id')
        source = self._build_node_obj(rel.start_node)
        target = self._build_node_obj(rel.end_node)
        return graph.Link(id, properties, source, target)
