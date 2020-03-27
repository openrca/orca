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

from orca.common.clients import rest_client


class PrometheusClient(rest_client.APIClient):

    """Client for Prometheus API."""

    def get_alerts(self):
        return self._connector.get("alerts")

    def instant_query(self, query):
        return self._connector.get("query", query=query)

    @classmethod
    def get(cls, url="http://localhost:9090", api_prefix="/api/v1"):
        connector = rest_client.APIConnector(url, api_prefix=api_prefix)
        return cls(connector)
