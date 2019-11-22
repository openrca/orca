from orca.graph.drivers.neo4j import Neo4jClient


class ClientFactory(object):

    @staticmethod
    def get_client(backend='neo4j'):
        if backend == 'neo4j':
            # TODO: read graph creds from config
            host = "orca-neo4j.rca"
            port = 7687
            user = "neo4j"
            password = "admin"
            return Neo4jClient(
                host=host, port=port, user=user, password=password)
