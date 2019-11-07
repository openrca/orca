from abc import ABC, abstractmethod


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
        self._handlers = []

    @staticmethod
    def create_node(id, metadata):
        return Node(id, metadata)

    @staticmethod
    def create_link(id, metadata, source, target):
        return Link(id, metadata, source, target)

    def get_nodes(self, metadata):
        return self._client.get_nodes(metadata)

    def get_node(self, id):
        return self._client.get_node(id)

    def add_node(self, node):
        self._client.add_node(node)
        for handler in self._handlers:
            handler.on_node_added(node)

    def update_node(self, node):
        self._client.update_node(node)
        for handler in self._handlers:
            handler.on_node_updatedd(node)

    def delete_node(self, node):
        links = self._client.get_node_links(node)
        for link in links:
            self._client.delete_link(link)
        self._client.delete(node)
        for handler in self._handlers:
            handler.on_node_deletedd(node)

    def get_links(self, metadata):
        self._client.get_links(metadata)

    def get_link(self, id):
        self._client.get_link(id)

    def add_link(self, link):
        self._client.add_link(link)

    def update_link(self, link):
        self._client.update_link(link)

    def delete_link(self, link):
        self._client.delete_link(link)

    def add_handler(self, handler):
        self._handlers.append(handler)


class EventHandler(ABC):

    def __init__(self, graph):
        self._graph = graph

    @abstractmethod
    def on_node_added(self, obj):
        pass

    @abstractmethod
    def on_node_updated(self, obj):
        pass

    @abstractmethod
    def on_node_deleted(self, obj):
        pass
