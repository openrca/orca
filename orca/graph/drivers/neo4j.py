import copy

import py2neo as graph_lib

from orca.graph import client


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
        nodes = self.client.nodes.match(**metadata)
        return list(map(self._build_node_obj, nodes))

    def get_node(self, id):
        node = self._get_node(id)
        return self._build_node_obj(node)

    def create_node(self, id, metadata):
        properties = copy.deepcopy(metadata)
        properties['_id'] = id
        node = graph_lib.Node(**properties)
        self.client.create(node)
        return self._build_node_obj(node)

    def update_node(self, id, metadata):
        node = self._get_node(id)
        node.update(metadata)
        self.client.push(node)
        return self._build_node_obj(node)

    def delete_node(self, id):
        node = self._get_node(id)
        rels = self._get_node_rels(node)
        for rel in rels:
            self.client.separate(rel)
        self.client.delete(node)

    def get_links(self, metadata=None):
        if not metadata:
            metadata = {}
        rels = self.client.relationships.match(**metadata)
        return list(map(self._build_link_obj, rels))

    def get_link(self, id):
        rel = self._get_rel(id)
        return self._build_link_obj(rel)

    def create_link(self, id, source_id, target_id, metadata):
        properties = copy.deepcopy(metadata)
        properties['_id'] = id
        source_node = self._get_node(source_id)
        target_node = self._get_node(target_id)
        rel = graph_lib.Relationship(source_node, target_node, **properties)
        self.client.create(rel)
        return self._build_link_obj(rel)

    def update_link(self, id, metadata):
        rel = self._get_rel(id)
        rel.update(metadata)
        self.client.push(rel)
        return self._build_link_obj(rel)

    def delete_link(self, id):
        rel = self._get_rel(id)
        self.client.separate(rel)

    def _get_node(self, id):
        return self.client.nodes.match(_id=id).first()

    def _get_node_rels(self, node):
        rels = self.client.relationships.match([node])
        return list(rels)

    def _get_rel(self, id):
        return self.client.relationships.match(_id=id)

    def _build_node_obj(self, node):
        properties = dict(node)
        id = properties.pop('_id')
        return client.Node(id, properties)

    def _build_link_obj(self, rel):
        properties = dict(rel)
        id = properties.pop('_id')
        source = self._build_node_obj(rel.start_node)
        target = self._build_node_obj(rel.end_node)
        return client.Link(id, properties, source, target)
