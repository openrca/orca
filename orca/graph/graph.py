import abc
import enum
import uuid

import addict as dictlib


class GraphObject(abc.ABC):

    def __init__(self, id, properties):
        super().__init__()
        self.id = id
        self.properties = dictlib.Dict(properties)


class Node(GraphObject):

    def __init__(self, id, properties, kind):
        super().__init__(id, properties)
        self.kind = kind

    def __repr__(self):
        return "<Node id=%s properties=%s kind=%s>" % (
            self.id, self.properties, self.kind)


class Link(GraphObject):

    def __init__(self, id, properties, source, target):
        super().__init__(id, properties)
        self.source = source
        self.target = target

    def __repr__(self):
        return "<Link id=%s properties=%s source=%s target=%s>" % (
            self.id, self.properties, self.source.id, self.target.id)


class Graph(object):

    def __init__(self, client):
        self._client = client
        self._listeners = []

    def get_nodes(self, kind=None, properties=None):
        return self._client.get_nodes(kind, properties)

    def get_node(self, id, kind=None, properties=None):
        return self._client.get_node(id, kind, properties)

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
        self._client.delete_node(node)
        self._notify_listeners(GraphEvent.NODE_DELETED, node)

    def get_links(self, properties=None):
        return self._client.get_links(properties)

    def get_link(self, id, properties=None):
        return self._client.get_link(id, properties)

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

    def get_node_links(self, node, kind=None):
        return self._client.get_node_links(node, kind)

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
    def create_node(id, kind, properties):
        return Node(id, properties, kind)

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


class GraphEvent(enum.Enum):

    NODE_ADDED = 1
    NODE_UPDATED = 2
    NODE_DELETED = 3
    LINK_ADDED = 4
    LINK_UPDATED = 5
    LINK_DELETED = 6


class EventListener(abc.ABC):

    def __init__(self, graph):
        super().__init__()
        self._graph = graph

    @abc.abstractmethod
    def on_node_added(self, node):
        pass

    @abc.abstractmethod
    def on_node_updated(self, node):
        pass

    @abc.abstractmethod
    def on_node_deleted(self, node):
        pass

    @abc.abstractmethod
    def on_link_added(self, link):
        pass

    @abc.abstractmethod
    def on_link_updated(self, link):
        pass

    @abc.abstractmethod
    def on_link_deleted(self, link):
        pass
