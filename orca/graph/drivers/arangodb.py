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

import copy

import arango

from orca.graph import graph
from orca.graph.drivers import driver
from orca.common import utils


class ArangoDBDriver(driver.Driver):

    """Arango Graph DB client."""

    def __init__(self, host, port, database, username=None, password=None):
        super().__init__()
        self._host = host
        self._port = port
        self._database_name = database
        self._username = username
        self._password = password
        self.__client = None
        self.__database = None
        self.__graph = None

    @property
    def _client(self):
        if not self.__client:
            self.__client = self._initialize_client()
        return self.__client

    @property
    def _database(self):
        if not self.__database:
            self.__database = self._initialize_database()
        return self.__database

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = self._initialize_graph()
        return self.__graph

    @property
    def _nodes(self):
        return self._graph.vertex_collection('nodes')

    @property
    def _links(self):
        return self._graph.edge_collection('links')

    def get_nodes(self, **query):
        query_pattern = ('FOR node in nodes %(filters)s RETURN node')
        filters = self._build_filters(query, handle='node')
        documents = self._execute_aql(query_pattern, filters=filters)
        return [self._build_node_obj(document) for document in documents]

    def get_node(self, node_id):
        document = self._nodes.get(node_id)
        if document:
            return self._build_node_obj(document)

    def add_node(self, node):
        document = self._build_node_doc(node)
        self._nodes.insert(document)

    def update_node(self, node):
        document = self._build_node_doc(node)
        self._nodes.update(document)

    def delete_node(self, node):
        self._nodes.delete(self._build_key(node))

    def get_links(self, **query):
        query_pattern = (
            'FOR link in links '
            '%(filters)s '
            'LET source = DOCUMENT(link._from) '
            'LET target = DOCUMENT(link._to)'
            'RETURN {link, source, target}')
        filters = self._build_filters(query, handle='link')
        documents = self._execute_aql(query_pattern, filters=filters)
        links = []
        for document in documents:
            link = self._build_link_obj(
                document['link'], document['source'], document['target'])
            links.append(link)
        return links

    def get_link(self, link_id):
        query_pattern = (
            'FOR link in links '
            'FILTER link._key == "%(link_id)s" '
            'LET source = DOCUMENT(link._from) '
            'LET target = DOCUMENT(link._to) '
            'LIMIT 1 '
            'RETURN {link, source, target}')
        documents = self._execute_aql(query_pattern, link_id=link_id)
        if not documents:
            return
        document = documents[0]
        return self._build_link_obj(
            document['link'], document['source'], document['target'])

    def add_link(self, link):
        document = self._build_link_doc(link)
        self._links.insert(document)

    def update_link(self, link):
        document = self._build_link_doc(link)
        self._links.update(document)

    def delete_link(self, link):
        self._links.delete(self._build_key(link))

    def get_node_links(self, node, **query):
        query_pattern = (
            'LET source = DOCUMENT("nodes/%(source_id)s") '
            'FOR target, link in 1..1 ANY source links '
            "%(filters)s "
            'RETURN {link, source, target}')
        filters = self._build_filters(query, handle='target')
        documents = self._execute_aql(
            query_pattern, source_id=node.id, filters=filters)
        links = []
        for document in documents:
            link = self._build_link_obj(
                document['link'], document['source'], document['target'])
            links.append(link)
        return links

    def _initialize_client(self):
        return arango.ArangoClient(hosts=self._get_db_uri())

    def _get_db_uri(self):
        return "http://%s:%s" % (self._host, self._port)

    def _initialize_database(self):
        sys_db = self._use_database('_system')
        if not sys_db.has_database(self._database_name):
            sys_db.create_database(self._database_name)
        return self._use_database(self._database_name)

    def _use_database(self, database):
        return self._client.db(
            database, username=self._username, password=self._password)

    def _initialize_graph(self):
        if not self._database.has_graph('graph'):
            self._database.create_graph('graph')
        graph = self._database.graph('graph')
        if not graph.has_vertex_collection('nodes'):
            graph.create_vertex_collection('nodes')
        if not graph.has_edge_definition('links'):
            graph.create_edge_definition(
                edge_collection='links',
                from_vertex_collections=['nodes'],
                to_vertex_collections=['nodes'])
        return graph

    def _build_key(self, graph_obj):
        return str(graph_obj.id)

    def _build_id(self, collection, graph_obj):
        return "%s/%s" % (collection, graph_obj.id)

    def _build_filters(self, query, handle):
        flatten_query = utils.flatten_dict(query, sep='.')
        filters = []
        for key, value in flatten_query.items():
            filters.append('FILTER %s.%s == "%s"' % (handle, key, value))
        return ' '.join(filters)

    def _execute_aql(self, query_pattern, **params):
        query = query_pattern % params
        cursor = self._database.aql.execute(query)
        return list(cursor)

    def _build_node_doc(self, node):
        document = {}
        document['_key'] = self._build_key(node)
        document['origin'] = node.origin
        document['kind'] = node.kind
        document['properties'] = copy.deepcopy(node.properties)
        return document

    def _build_node_obj(self, node_doc):
        node_id = node_doc.pop('_key')
        properties = node_doc.pop('properties')
        origin = node_doc.pop('origin')
        kind = node_doc.pop('kind')
        return graph.Node(node_id, properties, origin, kind)

    def _build_link_doc(self, link):
        document = {}
        document['_key'] = self._build_key(link)
        document['_from'] = self._build_id('nodes', link.source)
        document['_to'] = self._build_id('nodes', link.target)
        document['properties'] = copy.deepcopy(link.properties)
        return document

    def _build_link_obj(self, link_doc, source_doc, target_doc):
        link_id = link_doc.pop('_key')
        properties = link_doc.pop('properties')
        source_node = self._build_node_obj(source_doc)
        target_node = self._build_node_obj(target_doc)
        return graph.Link(link_id, properties, source_node, target_node)
