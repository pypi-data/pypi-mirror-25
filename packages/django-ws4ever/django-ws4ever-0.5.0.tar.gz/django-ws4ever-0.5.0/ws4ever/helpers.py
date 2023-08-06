import importlib

from django.conf import settings

from ws4ever.views import WebSocket404


def import_module(class_name):
    tokens = class_name.split('.')
    pkg = importlib.import_module('.'.join(tokens[:-1]))
    return getattr(pkg, tokens[-1])


def get_websocket_resources():
    resources = [(path, import_module(handler_class))
                 for path, handler_class in settings.WS4EVER['ROUTES'].items()]

    # 匹配不到404
    if not '.*' in settings.WS4EVER['ROUTES']:
        resources += [('.*', WebSocket404)]

    return resources


class ClientIndex:
    def __init__(self):
        self.dict = {}

    def get_all(self, key):
        return self.dict.get(key, set())

    def add(self, key, client):
        self.dict.setdefault(key, set()).add(client)

    def remove(self, key, client):
        clients = self.dict.get(key, set())
        clients -= {client}
        if not self.dict.get(key):
            self.dict.pop(key, None)
