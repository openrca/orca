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

from orca.common.clients.k8s import client as k8s


class ResourceProxyFactory(object):
    @staticmethod
    def get(kind):
        client = k8s.ClientFactory.get()
        if kind == "virtual_service":
            return k8s.CustomResourceProxy(
                kind="virtual_service",
                list_fn=client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="virtualservices",
            )
        elif kind == "destination_rule":
            return k8s.CustomResourceProxy(
                kind="destination_rule",
                list_fn=client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="destinationrules",
            )
        elif kind == "gateway":
            return k8s.CustomResourceProxy(
                kind="gateway",
                list_fn=client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="gateways",
            )
        else:
            raise Exception("Unknown kind %s" % kind)
