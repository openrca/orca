
from orca.graph.drivers import neo4j

host = "localhost"
port = 7687
user = "neo4j"
password = "admin"

g = neo4j.Neo4jClient(host, port, user, password)

from orca import graph

n1 = graph.Graph.create_node(123, 'pod', {})
g.add_node(n1)

n2 = graph.Graph.create_node(234, 'pod', {})
g.add_node(n2)

n3 = graph.Graph.create_node(345, 'pod', {})
g.add_node(n3)

g.get_nodes()
g.get_nodes(kind='pod')

l1 = graph.Graph.create_link({}, n1, n2)
g.add_link(l1)

l2 = graph.Graph.create_link({}, n1, n3)
g.add_link(l2)

g.get_links()

g.get_node_links(n1)
