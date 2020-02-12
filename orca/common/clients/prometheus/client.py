from orca.common.clients import client


class PrometheusClient(client.APIClient):

    def alerts(self):
        return self._connector.get("alerts")

    def instant_query(self, query):
        return self._connector.get("query", query=query)

    @staticmethod
    def get(url="http://localhost:9090", api_prefix="/api/v1"):
        connector = client.APIConnector(url, api_prefix=api_prefix)
        return PrometheusClient(connector)
