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

    def __init__(self, client, resource_kind, namespaced=True):
        self._client = client
        self._resource_kind = resource_kind
        self._namespaced = namespaced
        self._list_fn = self._get_list_fn()
        self._read_fn = self._get_read_fn()

    def _list(self):
        return self._list_fn()

    def _read(self, name, namespace=None):
        if self._namespaced:
            return self._read_fn(name, namespace)
        else:
            return self._read_fn(name)

    def _get_list_fn(self):
        fn_name = "list_%s" % self._resource_kind
        if self._namespaced:
            fn_name += "_for_all_namespaces"
        return getattr(self._client, fn_name)

    def _get_read_fn(self):
        fn_name = "read_"
        if self._namespaced:
            fn_name += "namespaced_"
        fn_name += self._resource_kind
        return getattr(self._client, fn_name)


class ResourceAPI(ResourceProxy):

    def get_all(self):
        return self._list().items

    def get(self, name, namespace):
        resource_obj = None
        try:
            resource_obj = self._read(name, namespace)
        except Exception as ex:
            log.error(str(ex))
        return resource_obj


class ResourceWatch(ResourceProxy):

    def __init__(self, client, resource_kind, namespaced=True):
        super().__init__(client, resource_kind, namespaced)
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
