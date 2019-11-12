from abc import ABC, abstractmethod
from enum import Enum

from kubernetes import client, config, watch

from orca.common import logger

log = logger.get_logger(__name__)


class ClientFactory(object):

    @staticmethod
    def get_client():
        config.load_incluster_config()
        return client


class ResourceProxy(object):

    def __init__(self, client, resource_type):
        self._client = client
        self._resource_type = resource_type
        self._list_fn = self._get_list_fn(resource_type)
        self._read_fn = self._get_read_fn(resource_type)

    @property
    def resource_type(self):
        return self._resource_type

    def _get_list_fn(self, resource_type):
        return getattr(
            self._client, "list_%s_for_all_namespaces" % resource_type)

    def _get_read_fn(self, resource_type):
        return getattr(
            self._client, "read_namespaced_%s" % resource_type)


class ResourceAPI(ResourceProxy):

    def get_all(self):
        return self._list_fn().items

    def get(self, name, namespace):
        resource_obj = None
        try:
            resource_obj = self._read_fn(name, namespace)
        except Exception as ex:
            log.error(str(ex))
        return resource_obj

    def get_by_node(self, node):
        name = node.metadata['name']
        namespace = node.metadata['namespace']
        return self.get(name, namespace)


class ResourceWatch(ResourceProxy):

    def __init__(self, client, resource_type):
        super().__init__(client, resource_type)
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)

    def run(self):
        resource_watch = watch.Watch()
        for event in resource_watch.stream(self._list_fn):
            self._handle_event(event)

    def _handle_event(self, event):
        event_type = event['type']
        resource_obj = event['object']
        for handler in self._handlers:
            if event_type == "ADDED":
                handler.on_added(resource_obj)
            if event_type == "UPDATED":
                handler.on_updated(resource_obj)
            if event_type == "DELETED":
                handler.on_deleted(resource_obj)


class EventHandler(ABC):

    @abstractmethod
    def on_added(self, obj):
        """Triggered when a K8S resource is added."""

    @abstractmethod
    def on_updated(self, obj):
        """Triggered when a K8S resource is updated."""

    @abstractmethod
    def on_deleted(self, obj):
        """Triggered when a K8S resource is deleted."""




