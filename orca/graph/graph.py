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

import abc
import enum
import uuid
import contextlib

import addict as dictlib

from orca.common import config, logger, utils
from orca.graph import drivers

CONFIG = config.CONFIG
LOG = logger.get_logger(__name__)


class GraphObject(abc.ABC):
    def __init__(self, id, properties, **kwargs):
        super().__init__()
        self.id = id
        self.properties = dictlib.Dict(properties)
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.deleted_at = kwargs.get("deleted_at")


class Node(GraphObject):
    def __init__(self, id, properties, origin, kind, **kwargs):
        super().__init__(id, properties, **kwargs)
        self.origin = origin
        self.kind = kind

    def __repr__(self):
        return "<Node id=%s properties=%s kind=%s>" % (
            self.id,
            self.properties,
            self.kind,
        )


class Link(GraphObject):
    def __init__(self, id, properties, source, target, **kwargs):
        super().__init__(id, properties, **kwargs)
        self.source = source
        self.target = target

    def __repr__(self):
        return "<Link id=%s properties=%s source=%s target=%s>" % (
            self.id,
            self.properties,
            self.source.id,
            self.target.id,
        )


class Graph(object):
    def __init__(self, driver, lock):
        self._driver = driver
        self._lock = lock
        self._listeners = []

    @contextlib.contextmanager
    def locked(self):
        self.lock()
        try:
            yield self
        finally:
            self.unlock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def setup(self):
        LOG.info("Initializing graph database")
        self._driver.setup()

    def get_nodes(self, time_point=None, properties=None, include_deleted=False):
        if not properties:
            properties = {}
        return self._driver.get_nodes(time_point, properties, include_deleted)

    def get_node(self, node_id):
        return self._driver.get_node(node_id)

    def add_node(self, node):
        if self.get_node(node.id):
            return
        node.created_at = utils.get_utc()
        node.updated_at = node.created_at
        LOG.debug("Adding node: %s", node)
        self._driver.add_node(node)
        self._notify_listeners(GraphEvent.NODE_ADDED, node)

    def update_node(self, new_node):
        node = self.get_node(new_node.id)
        if not node:
            return
        node.properties = new_node.properties
        node.updated_at = utils.get_utc()
        LOG.debug("Updating node: %s", node)
        self._driver.update_node(node)
        self._notify_listeners(GraphEvent.NODE_UPDATED, node)

    def delete_node(self, node_id):
        node = self.get_node(node_id)
        if not node:
            return
        links = self._driver.get_node_links(node)
        for link in links:
            self.delete_link(link.id)
        node.deleted_at = utils.get_utc()
        LOG.debug("Deleting node: %s", node)
        self._driver.update_node(node)
        self._notify_listeners(GraphEvent.NODE_DELETED, node)

    def get_links(self, time_point=None, properties=None, include_deleted=False):
        if not properties:
            properties = {}
        return self._driver.get_links(time_point, properties, include_deleted)

    def get_link(self, link_id):
        return self._driver.get_link(link_id)

    def add_link(self, link):
        if self.get_link(link.id):
            return
        link.created_at = utils.get_utc()
        link.updated_at = link.created_at
        LOG.debug("Adding link: %s", link)
        self._driver.add_link(link)
        self._notify_listeners(GraphEvent.LINK_ADDED, link)

    def update_link(self, new_link):
        link = self.get_link(new_link.id)
        if not link:
            return
        link.properties = new_link.properties
        link.updated_at = utils.get_utc()
        LOG.debug("Updating link: %s", new_link)
        self._driver.update_link(link)
        self._notify_listeners(GraphEvent.LINK_UPDATED, link)

    def delete_link(self, link_id):
        link = self.get_link(link_id)
        if not link:
            return
        link.deleted_at = utils.get_utc()
        LOG.debug("Deleting link: %s", link)
        self._driver.update_link(link)
        self._notify_listeners(GraphEvent.LINK_DELETED, link)

    def get_node_links(self, node, **query):
        return self._driver.get_node_links(node, **query)

    def add_listener(self, listener):
        self._listeners.append(listener)

    def _notify_listeners(self, event_type, graph_obj):
        for listener in self._listeners:
            if event_type == GraphEvent.NODE_ADDED:
                listener.on_node_added(graph_obj)
            elif event_type == GraphEvent.NODE_UPDATED:
                listener.on_node_updated(graph_obj)
            elif event_type == GraphEvent.NODE_DELETED:
                listener.on_node_deleted(graph_obj)
            elif event_type == GraphEvent.LINK_ADDED:
                listener.on_link_added(graph_obj)
            elif event_type == GraphEvent.LINK_UPDATED:
                listener.on_link_updated(graph_obj)
            elif event_type == GraphEvent.LINK_DELETED:
                listener.on_link_deleted(graph_obj)
            else:
                raise Exception("Unknown event type: %s" % event_type)

    @classmethod
    def get(cls, lock):
        driver = drivers.DriverFactory.get(CONFIG.graph.driver)
        return cls(driver, lock)

    @staticmethod
    def create_node(id, properties, origin, kind):
        return Node(id, properties, origin, kind)

    @staticmethod
    def create_link(properties, source, target):
        id = Graph.generate_id(source.id, target.id)
        return Link(id, properties, source, target)

    @staticmethod
    def generate_id(*names):
        if names:
            namespace = uuid.NAMESPACE_OID
            name = "/".join([str(name) for name in names])
            id = uuid.uuid5(namespace, name)
        else:
            id = uuid.uuid4()
        return str(id)


class EventListener(abc.ABC):
    @abc.abstractmethod
    def on_node_added(self, node):
        """Callback triggered when graph node is added."""

    @abc.abstractmethod
    def on_node_updated(self, node):
        """Callback triggered when graph node is updated."""

    @abc.abstractmethod
    def on_node_deleted(self, node):
        """Callback triggered when graph node is deleted."""

    @abc.abstractmethod
    def on_link_added(self, link):
        """Callback triggered when graph link is added."""

    @abc.abstractmethod
    def on_link_updated(self, link):
        """Callback triggered when graph link is updated."""

    @abc.abstractmethod
    def on_link_deleted(self, link):
        """Callback triggered when graph link is deleted."""


class GraphEvent(enum.Enum):

    NODE_ADDED = 1
    NODE_UPDATED = 2
    NODE_DELETED = 3
    LINK_ADDED = 4
    LINK_UPDATED = 5
    LINK_DELETED = 6
