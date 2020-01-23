import json

import neo4j as graph_lib

from orca.graph import graph
from orca.graph.drivers import driver


class Neo4jDriver(driver.Driver):

    """Neo4j Graph DB client."""

    def __init__(self, host, port, user=None, password=None):
        super().__init__()
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._client = None

    @property
    def client(self):
        if not self._client:
            uri = self._get_db_uri()
            auth = self._get_db_auth()
            self._client = graph_lib.GraphDatabase.driver(uri, auth=auth)
        return self._client

    def get_nodes(self, kind=None, properties=None):
        node_pattern = self._build_node_pattern(None, kind, None)
        query = "MATCH %s RETURN node" % (node_pattern)
        query_result = self._run_query(query)
        records = query_result.records()
        nodes = [record['node'] for record in records]
        return list(map(self._build_node_obj, nodes))

    def get_node(self, id, kind=None, properties=None):
        node_pattern = self._build_node_pattern(id, kind, None)
        query = "MATCH %s RETURN node LIMIT 1" % (node_pattern)
        query_result = self._run_query(query)
        record = query_result.single()
        if record:
            return self._build_node_obj(record['node'])

    def add_node(self, node):
        properties = {'properties': json.dumps(node.properties)}
        node_pattern = self._build_node_pattern(node.id, node.kind, properties)
        query = "CREATE %s" % (node_pattern)
        self._run_query(query)

    def update_node(self, node):
        pass

    def delete_node(self, node):
        node_pattern = self._build_node_pattern(node.id, node.kind, None)
        query = "MATCH %s DETACH DELETE node" % (node_pattern)
        self._run_query(query)

    def get_links(self, properties=None):
        rel_pattern = self._build_rel_pattern(None, "linked", properties)
        query = ("MATCH (src_node)-%s->(dst_node) "
                 "RETURN rel, src_node, dst_node") % (rel_pattern)
        query_result = self._run_query(query)
        records = query_result.records()
        links = []
        for record in records:
            link = self._build_link_obj(
                record['rel'], record['src_node'], record['dst_node'])
            links.append(link)
        return links

    def get_link(self, id, properties=None):
        rel_pattern = self._build_rel_pattern(id, "linked", properties)
        query = ("MATCH (src_node)-%s-(dst_node) "
                 "RETURN rel, src_node, dst_node LIMIT 1") % (rel_pattern)
        query_result = self._run_query(query)
        record = query_result.single()
        if record:
            return self._build_link_obj(
                record['rel'], record['src_node'], record['dst_node'])

    def add_link(self, link):
        source_node = link.source
        target_node = link.target
        source_node_pattern = self._build_node_pattern(
            source_node.id, source_node.kind, None,
            var_name="src_node")
        target_node_pattern = self._build_node_pattern(
            target_node.id, target_node.kind, None,
            var_name="dst_node")
        rel_pattern = self._build_rel_pattern(link.id, "linked", link.properties)
        query = "MATCH %s, %s CREATE (src_node)-%s->(dst_node)" % (
            source_node_pattern, target_node_pattern, rel_pattern)
        self._run_query(query)

    def update_link(self, link):
        pass

    def delete_link(self, link):
        rel_pattern = self._build_rel_pattern(link.id, "linked", link.properties)
        query = "MATCH (src_node)-%s-(dst_node) DELETE rel" % (rel_pattern)
        self._run_query(query)

    def get_node_links(self, node, kind=None):
        source_node_pattern = self._build_node_pattern(
            node.id, node.kind, None, var_name="src_node")
        target_node_pattern = self._build_node_pattern(
            None, kind, None, var_name="dst_node")
        query = ("MATCH %s-[rel:linked]-%s "
                 "RETURN rel, src_node, dst_node") % (
                     source_node_pattern, target_node_pattern)
        query_result = self._run_query(query)
        records = query_result.records()
        links = []
        for record in records:
            link = self._build_link_obj(
                record['rel'], record['src_node'], record['dst_node'])
            links.append(link)
        return links

    def _get_db_uri(self):
        return "bolt://%s:%s" % (self._host, self._port)

    def _get_db_auth(self):
        return (self._user, self._password)

    def _build_cypher_labels(self, labels):
        return "".join([":%s" % label for label in labels if label])

    def _build_cypher_properties(self, properties):
        prop_items = []
        for key, value in properties.items():
            prop_item = "%s: '%s'" % (key, value)
            prop_items.append(prop_item)
        return ", ".join(prop_items)

    def _build_node_pattern(self, id, kind, properties, var_name="node"):
        inner_pattern = self._build_obj_inner_pattern(
            id, kind, properties, var_name)
        return "(%s)" % (inner_pattern)

    def _build_rel_pattern(self, id, kind, properties, var_name="rel"):
        inner_pattern = self._build_obj_inner_pattern(
            id, kind, properties, var_name)
        return "[%s]" % (inner_pattern)

    def _build_obj_inner_pattern(self, id, kind, properties, var_name):
        if not properties:
            properties = {}
        cypher_labels = self._build_cypher_labels([kind])
        if id:
            properties['id'] = id
        cypher_properties = self._build_cypher_properties(properties)
        return "%s%s {%s}" % (var_name, cypher_labels, cypher_properties)

    def _run_query(self, query, values=None):
        result = None
        with self.client.session() as session:
            result = session.run(query, values)
        return result

    def _build_node_obj(self, node):
        raw_properties = dict(node.items())
        id = raw_properties.pop('id')
        properties = json.loads(raw_properties['properties'])
        kind = list(node.labels)[0]
        return graph.Node(id, properties, kind)

    def _build_link_obj(self, rel, src_node, dst_node):
        properties = dict(rel.items())
        id = properties.pop('id')
        source = self._build_node_obj(src_node)
        target = self._build_node_obj(dst_node)
        return graph.Link(id, properties, source, target)
