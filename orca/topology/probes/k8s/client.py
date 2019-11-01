from abc import ABC, abstractmethod

from kubernetes import client, config, watch


class ClientFactory(object):

    @staticmethod
    def get_client():
        config.load_incluster_config()
        return client.CoreV1Api()


class Watch(object):

    def __init__(self, resource_api, handler):
        self._resource_api = resource_api
        self._handler = handler

    def run(self):
        resource_watch = watch.Watch()
        for event in resource_watch.stream(self._resource_api):
            self._handle_event(event)

    def _handle_event(self, event):
        event_type = event['type']
        obj = event['object']
        if event_type == 'ADD':
            self._handler.on_add(obj)
        elif event_type == 'UPDATE':
            self._handler.on_update(obj)
        elif event_type == 'DELETE':
            self._handler.on_delete(obj)
        else:
            raise Exception("Unknown event type: %s" % event_type)


class EventHandler(ABC):

    @abstractmethod
    def on_add(self, obj):
        pass

    @abstractmethod
    def on_update(self, obj):
        pass

    @abstractmethod
    def on_delete(self, obj):
        pass
