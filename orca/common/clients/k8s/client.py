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

import addict as dictlib
from kubernetes import client, config, watch

from orca.common import logger
from orca.common.clients.k8s import exceptions

LOG = logger.get_logger(__name__)


class ClientFactory(object):
    @staticmethod
    def get():
        config.load_incluster_config()
        return client


class ResourceProxyFactory(object):
    @staticmethod
    def get(kind):
        client = ClientFactory.get()
        if kind == "pod":
            return ResourceProxy(
                kind="pod", list_fn=client.CoreV1Api().list_pod_for_all_namespaces
            )
        elif kind == "service":
            return ResourceProxy(
                kind="service",
                list_fn=client.CoreV1Api().list_service_for_all_namespaces,
            )
        elif kind == "endpoints":
            return ResourceProxy(
                kind="endpoints",
                list_fn=client.CoreV1Api().list_endpoints_for_all_namespaces,
            )
        elif kind == "config_map":
            return ResourceProxy(
                kind="config_map",
                list_fn=client.CoreV1Api().list_config_map_for_all_namespaces,
            )
        elif kind == "secret":
            return ResourceProxy(
                kind="secret", list_fn=client.CoreV1Api().list_secret_for_all_namespaces
            )
        elif kind == "node":
            return ResourceProxy(kind="node", list_fn=client.CoreV1Api().list_node)
        elif kind == "deployment":
            return ResourceProxy(
                kind="deployment",
                list_fn=client.AppsV1Api().list_deployment_for_all_namespaces,
            )
        elif kind == "stateful_set":
            return ResourceProxy(
                kind="stateful_set",
                list_fn=client.AppsV1Api().list_stateful_set_for_all_namespaces,
            )
        elif kind == "daemon_set":
            return ResourceProxy(
                kind="daemon_set",
                list_fn=client.AppsV1Api().list_daemon_set_for_all_namespaces,
            )
        elif kind == "replica_set":
            return ResourceProxy(
                kind="replica_set",
                list_fn=client.AppsV1Api().list_replica_set_for_all_namespaces,
            )
        elif kind == "storage_class":
            return ResourceProxy(
                kind="storage_class", list_fn=client.StorageV1Api().list_storage_class
            )
        elif kind == "persistent_volume":
            return ResourceProxy(
                kind="persistent_volume",
                list_fn=client.CoreV1Api().list_persistent_volume,
            )
        elif kind == "persistent_volume_claim":
            return ResourceProxy(
                kind="persistent_volume_claim",
                list_fn=client.CoreV1Api().list_persistent_volume_claim_for_all_namespaces,
            )
        elif kind == "namespace":
            return ResourceProxy(
                kind="namespace", list_fn=client.CoreV1Api().list_namespace
            )
        elif kind == "horizontal_pod_autoscaler":
            return ResourceProxy(
                kind="horizontal_pod_autoscaler",
                list_fn=client.AutoscalingV1Api().list_horizontal_pod_autoscaler_for_all_namespaces,
            )
        elif kind == "ingress":
            return ResourceProxy(
                kind="ingress",
                list_fn=client.ExtensionsV1beta1Api().list_ingress_for_all_namespaces,
            )
        elif kind == "job":
            return ResourceProxy(
                kind="job", list_fn=client.BatchV1Api().list_job_for_all_namespaces
            )
        elif kind == "cron_job":
            return ResourceProxy(
                kind="cron_job",
                list_fn=client.BatchV1beta1Api().list_cron_job_for_all_namespaces,
            )
        else:
            raise Exception("Unknown kind %s" % kind)


class ResourceProxy(object):
    def __init__(self, kind, list_fn):
        self._kind = kind
        self._list_fn = list_fn

    def get_all(self):
        return self._list_fn().items

    def watch(self):
        while True:
            LOG.debug("Restarting watch for resource kind: %s", self._kind)
            for event in self._watch_resource():
                event_type, event_obj = event["type"], event["object"]

                # "410 Gone" is for the "resource version too old" error, we must restart watching.
                # The error occurs when the watch stream is inactive for more than a few minutes.
                if event_type == "ERROR" and event_obj.code == 410:
                    break

                # Other watch errors should be fatal for the consumer.
                if event_type == "ERROR":
                    raise exceptions.WatchError(reason=event_obj.message)

                # Ensure that the event is something we understand and can handle.
                if event_type not in ["ADDED", "MODIFIED", "DELETED"]:
                    raise exceptions.UnknownWatchEvent(event_type=event_type)

                # Yield normal events to the consumer. Errors are already filtered out.
                yield event

    def _watch_resource(self):
        return watch.Watch().stream(self._list_fn)


class CustomResourceProxy(ResourceProxy):
    def __init__(self, kind, list_fn, group, version, plural):
        super().__init__(kind, list_fn)
        self._group = group
        self._version = version
        self._plural = plural

    def get_all(self):
        items = self._list_fn(self._group, self._version, self._plural)["items"]
        return [self._extract_item(item) for item in items]

    def _watch_resource(self):
        for event in watch.Watch().stream(
            self._list_fn, self._group, self._version, self._plural
        ):
            event["object"] = self._extract_item(event.pop("object"))
            yield event

    def _extract_item(self, item):
        return dictlib.Dict(item)
