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

from requests import auth

from orca.common.clients import rest_client


class KialiClient(rest_client.APIClient):

    """Client for Kiali API."""

    def list_namespaces(self):
        return self._connector.get("/namespaces")

    def graph_namespaces(self, namespaces, graph_type="service"):
        namespace_list = ",".join(namespaces)
        return self._connector.get(
            "/namespaces/graph", namespaces=namespace_list, graphType=graph_type
        )

    @classmethod
    def get(
        cls, url="http://localhost:20001", api_prefix="/kiali/api", username=None, password=None
    ):
        basic_auth = None
        if username and password:
            basic_auth = auth.HTTPBasicAuth(username, password)
        connector = rest_client.APIConnector(url, api_prefix=api_prefix, auth=basic_auth)
        return cls(connector)
