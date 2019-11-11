import uuid

from abc import ABC, abstractmethod
from enum import Enum


class GraphObject(ABC):

    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata


class Node(GraphObject):

    def __init__(self, id, metadata):
        super().__init__(id, metadata)

    def __repr__(self):
        return "<Node id=%s metadata=%s>" % (self.id, self.metadata)


class Link(GraphObject):

    def __init__(self, id, metadata, source, target):
        super().__init__(id, metadata)
        self.source = source
        self.target = target

    def __repr__(self):
        return "<Link id=%s metadata=%s source=%s target=%s>" % (
            self.id, self.metadata, self.source.id, self.target.id)


class Graph(object):

    def __init__(self, client):
        self._client = client
        self._listeners = []

    def get_nodes(self, metadata):
        return self._client.get_nodes(metadata)

    def get_node(self, id):
        return self._client.get_node(id)

    def add_node(self, node):
        if self.get_node(node.id):
            return
        self._client.add_node(node)
        self._notify_listeners(GraphEvent.NODE_ADDED, node)

    def update_node(self, node):
        self._client.update_node(node)
        self._notify_listeners(GraphEvent.NODE_UPDATED, node)

    def delete_node(self, node):
        links = self._client.get_node_links(node)
        for link in links:
            self._client.delete_link(link)
        self._client.delete(node)
        self._notify_listeners(GraphEvent.NODE_DELETED, node)

    def get_links(self, metadata):
        return self._client.get_links(metadata)

    def get_link(self, id):
        return self._client.get_link(id)

    def add_link(self, link):
        if self.get_link(link.id):
            return
        self._client.add_link(link)
        self._notify_listeners(GraphEvent.LINK_ADDED, link)

    def update_link(self, link):
        self._client.update_link(link)
        self._notify_listeners(GraphEvent.LINK_UPDATED, link)

    def delete_link(self, link):
        self._client.delete_link(link)
        self._notify_listeners(GraphEvent.LINK_DELETED, link)

    def get_node_links(self, node):
        return self._client.get_node_links(node)

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

    @staticmethod
    def create_node(id, metadata):
        return Node(id, metadata)

    @staticmethod
    def create_link(metadata, source, target):
        id = Graph.generate_id(source.id, target.id)
        return Link(id, metadata, source, target)

    @staticmethod
    def generate_id(*names):
        if names:
            namespace = uuid.NAMESPACE_OID
            name = "/".join(names)
            id = uuid.uuid5(namespace, name)
        else:
            id = uuid.uuid4()
        return str(id)


class GraphEvent(Enum):

    NODE_ADDED = 1
    NODE_UPDATED = 2
    NODE_DELETED = 3
    LINK_ADDED = 4
    LINK_UPDATED = 5
    LINK_DELETED = 6


class EventListener(ABC):

    def __init__(self, graph):
        self._graph = graph

    @abstractmethod
    def on_node_added(self, node):
        pass

    @abstractmethod
    def on_node_updated(self, node):
        pass

    @abstractmethod
    def on_node_deleted(self, node):
        pass

    @abstractmethod
    def on_link_added(self, link):
        pass

    @abstractmethod
    def on_link_updated(self, link):
        pass

    @abstractmethod
    def on_link_deleted(self, link):
        pass
