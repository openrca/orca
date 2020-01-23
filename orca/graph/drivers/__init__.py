from orca.graph.drivers.neo4j import Neo4jDriver


class DriverFactory(object):

    @staticmethod
    def get(backend='neo4j'):
        if backend == 'neo4j':
            # TODO: read graph creds from config
            host = "orca-neo4j.rca"
            port = 7687
            user = "neo4j"
            password = "admin"
            return Neo4jDriver(
                host=host, port=port, user=user, password=password)
