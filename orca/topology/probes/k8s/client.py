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
        self._handler_func_mapping = self._get_handler_func_mapping()

    def run(self):
        resource_watch = watch.Watch()
        for event in resource_watch.stream(self._resource_api):
            self._handle_event(event)

    def _get_handler_func_mapping(self):
        return {
            'ADD': self._handler.on_add,
            'UPDATE': self._handler.on_update,
            'DELETE': self._handler.on_delete
        }

    def _handle_event(self, event):
        event_type = event['type']
        resource_object = event['object']
        try:
            handler_func = self._handler_func_mapping[event_type]
            handler_func(resource_object)
        except KeyError:
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
