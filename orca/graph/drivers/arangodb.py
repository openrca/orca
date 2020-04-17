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
import json

import arango

from orca.common import utils
from orca.graph import graph
from orca.graph.drivers import driver


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
            self.__client = self._get_client()
        return self.__client

    @property
    def _database(self):
        if not self.__database:
            self.__database = self._use_database(self._database_name)
        return self.__database

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = self._use_graph('graph')
        return self.__graph

    def setup(self):
        sys_db = self._use_database('_system')
        if not sys_db.has_database(self._database_name):
            sys_db.create_database(self._database_name)
        db = self._use_database(self._database_name)

        if not db.has_graph('graph'):
            db.create_graph('graph')
        graph = db.graph('graph')

        if not graph.has_vertex_collection('nodes'):
            graph.create_vertex_collection('nodes')
        if not graph.has_edge_definition('links'):
            graph.create_edge_definition(
                edge_collection='links',
                from_vertex_collections=['nodes'],
                to_vertex_collections=['nodes'])

        nodes_col = graph.vertex_collection('nodes')
        nodes_col.add_hash_index(fields=['id'], unique=False)

        links_col = graph.edge_collection('links')
        links_col.add_hash_index(fields=['id'], unique=False)


    def get_nodes(self, **query):
        query_pattern = (
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            '%(filters)s '
            'RETURN node')
        filters = self._build_filters(query, handle='node')
        documents = self._execute_aql(query_pattern, filters=filters)
        return [self._build_node_obj(document) for document in documents]

    def get_node(self, node_id):
        query_pattern = (
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            'FILTER node.id == "%(node_id)s" '
            'LIMIT 1 '
            'RETURN node')
        documents = self._execute_aql(query_pattern, node_id=node_id)
        if documents:
            return self._build_node_obj(documents[0])

    def add_node(self, node):
        query_pattern = (
            'INSERT %(document)s INTO nodes')
        document = self._serialize_node(node)
        self._execute_aql(query_pattern, document=document)

    def update_node(self, node):
        query_pattern = (
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            'FILTER node.id == "%(node_id)s" '
            'UPDATE node WITH %(document)s IN nodes')
        document = self._serialize_node(node)
        self._execute_aql(query_pattern, node_id=node.id, document=document)

    def delete_node(self, node):
        query_pattern = (
            'FOR node in nodes '
            'FILTER node.id == "%(node_id)s" '
            'REMOVE node IN nodes')
        self._execute_aql(query_pattern, node_id=node.id)

    def get_links(self, **query):
        query_pattern = (
            'FOR link in links '
            'FILTER link.deleted_at == null '
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
            'FILTER link.deleted_at == null '
            'FILTER link.id == "%(link_id)s" '
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
        query_pattern = (
            'LET source = FIRST( '
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            'FILTER node.id == "%(source_id)s" '
            'LIMIT 1 RETURN node) '
            'LET target = FIRST( '
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            'FILTER node.id == "%(target_id)s" '
            'LIMIT 1 RETURN node) '
            'LET link = MERGE(%(document)s, {"_from": source._id, "_to": target._id})'
            'INSERT link INTO links')
        document = self._serialize_link(link)
        self._execute_aql(
            query_pattern, source_id=link.source.id, target_id=link.target.id, document=document)

    def update_link(self, link):
        query_pattern = (
            'FOR link IN links '
            'FILTER link.deleted_at == null '
            'FILTER link.id == "%(link_id)s" '
            'UPDATE link WITH %(document)s IN links')
        document = self._serialize_link(link)
        self._execute_aql(query_pattern, link_id=link.id, document=document)

    def delete_link(self, link):
        query_pattern = (
            'FOR link in links '
            'FILTER link.id == "%(link_id)s" '
            'REMOVE link IN links')
        self._execute_aql(query_pattern, link_id=link.id)

    def get_node_links(self, node, **query):
        query_pattern = (
            'LET source = FIRST( '
            'FOR node in nodes '
            'FILTER node.deleted_at == null '
            'FILTER node.id == "%(source_id)s" '
            'LIMIT 1 RETURN node) '
            'FOR target, link in 1..1 ANY source links '
            'FILTER link.deleted_at == null '
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

    def _get_client(self):
        return arango.ArangoClient(hosts=self._get_db_uri())

    def _get_db_uri(self):
        return "http://%s:%s" % (self._host, self._port)

    def _use_database(self, database):
        return self._client.db(
            database, username=self._username, password=self._password)

    def _use_graph(self, graph):
        return self._database.graph(graph)

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

    def _serialize_node(self, node):
        document = {}
        document['id'] = node.id
        document['origin'] = node.origin
        document['kind'] = node.kind
        document['properties'] = copy.deepcopy(node.properties)
        document['created_at'] = node.created_at
        document['updated_at'] = node.updated_at
        document['deleted_at'] = node.deleted_at
        return json.dumps(document)

    def _build_node_obj(self, node_doc):
        node_id = node_doc.pop('id')
        properties = node_doc.pop('properties')
        origin = node_doc.pop('origin')
        kind = node_doc.pop('kind')
        created_at = node_doc.pop('created_at')
        updated_at = node_doc.pop('updated_at')
        deleted_at = node_doc.pop('deleted_at')
        return graph.Node(
            node_id, properties, origin, kind,
            created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)

    def _serialize_link(self, link):
        document = {}
        document['id'] = link.id
        document['properties'] = copy.deepcopy(link.properties)
        document['created_at'] = link.created_at
        document['updated_at'] = link.updated_at
        document['deleted_at'] = link.deleted_at
        return json.dumps(document)

    def _build_link_obj(self, link_doc, source_doc, target_doc):
        link_id = link_doc.pop('id')
        properties = link_doc.pop('properties')
        source_node = self._build_node_obj(source_doc)
        target_node = self._build_node_obj(target_doc)
        created_at = link_doc.pop('created_at')
        updated_at = link_doc.pop('updated_at')
        deleted_at = link_doc.pop('deleted_at')
        return graph.Link(
            link_id, properties, source_node, target_node,
            created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)
