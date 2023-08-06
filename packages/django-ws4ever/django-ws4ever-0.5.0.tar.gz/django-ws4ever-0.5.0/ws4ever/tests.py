import time
import ujson as json
from functools import partial
from typing import Any, Optional
from unittest.mock import MagicMock, PropertyMock, patch

import gevent
import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management import call_command
from django.test import LiveServerTestCase, TestCase, override_settings
from websocket import create_connection

from django_ws4ever.wsgi import application
from ws4ever.backend import get_backend, notify_clients
from ws4ever.helpers import ClientIndex
from ws4ever.management.commands.runserver import get_server
from ws4ever.views import BaseWebSocketApplication

User = get_user_model()


class WaitableMock:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        def make_func(*args, **kwargs):
            ret = self.func(*args, **kwargs)
            make_func.called = True
            return ret

        make_func.wait_called = partial(self.wait_called, make_func)

        return make_func

    @classmethod
    def wait_called(cls, func, timeout=5):
        exception = Exception('{} timeout'.format(func))
        with gevent.Timeout(timeout, exception):
            while not getattr(func, 'called', False):
                gevent.sleep()
        return True


class WS4EverServerTestCase(LiveServerTestCase):
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8727

    @classmethod
    def _create_server_thread(cls, connections_override):
        class MyLiveServerThread(object):
            is_ready = MagicMock()
            is_ready.wait = MagicMock()
            join = MagicMock()
            error = None
            httpd = None

            def start(self):
                self.httpd = get_server(cls.SERVER_HOST, cls.SERVER_PORT,
                                        StaticFilesHandler(application))
                gevent.spawn(self.httpd.serve_forever)

            def terminate(self):
                self.httpd.stop(1)

        return MyLiveServerThread()


class TestWebsocketApplication(BaseWebSocketApplication):
    def handle_message(self, kind: str, payload: Optional[Any] = None):
        self.send_message(kind, payload)

    @classmethod
    def on_notify(cls, kind, payload, **extra):
        for client in cls.clients.values():
            client.send_message(kind, payload=payload)


@override_settings(WS4EVER={
    'ROUTES': {
        "/ws": "ws4ever.tests.TestWebsocketApplication"
    },
    'MAX_IDLE': 0.2,
    'NOTIFY_BACKEND': 'redis://127.0.0.1:6379/1'
})
class RedisWebSocketApplicationTests(WS4EverServerTestCase):
    @classmethod
    def connect(cls):
        ws_url = 'ws://{}:{}{}'.format(cls.SERVER_HOST, cls.SERVER_PORT,
                                       list(settings.WS4EVER['ROUTES'].keys())[0])
        conn = create_connection(ws_url)
        gevent.sleep(0.1)
        return conn

    @classmethod
    def clients(cls):
        return list(TestWebsocketApplication.clients.values())

    def test_send_message_to(self):
        ws = self.connect()
        payload = {"kind": "hello", "payload": "world"}

        ws.send(json.dumps({"kind": "hello", "payload": "world"}))
        self.assertEqual(json.loads(ws.recv()), payload, "得到了message")
        ws.close()

    def test_publish_client_message(self):
        with patch('redis.client.PubSub.psubscribe',
                   new_callable=WaitableMock(redis.client.PubSub.psubscribe)) as mocked_method:
            gevent.spawn(get_backend)
            mocked_method.wait_called()
        ws = self.connect()
        data = {"kind": "hello", "payload": "world"}

        notify_clients("hello", "world", a='b')
        self.assertEqual(json.loads(ws.recv()), data, "得到了message")
        ws.close()

    def test_kill_zombies(self):
        class FakeClient:
            def __init__(self):
                self.last_ping = 0
                self.close = MagicMock()

        client_zombie = FakeClient()

        client_pinged = FakeClient()
        client_pinged.last_ping = time.time()

        fake_clients = {1: client_pinged, 2: client_zombie}

        with patch('ws4ever.tests.TestWebsocketApplication.clients',
                   new_callable=PropertyMock, return_value=fake_clients):
            TestWebsocketApplication.check_zombie_clients.delete_memoized()
            TestWebsocketApplication.check_zombie_clients()
            client_pinged.close.assert_not_called()
            client_zombie.close.assert_called_with()


@override_settings(WS4EVER={
    'ROUTES': {
        "/ws": "ws4ever.tests.TestWebsocketApplication"
    },
    'MAX_IDLE': 0.2,
    'NOTIFY_BACKEND': 'memory'
})
class MemoryWebSocketApplicationTests(WS4EverServerTestCase):
    @classmethod
    def connect(cls):
        ws_url = 'ws://{}:{}{}'.format(cls.SERVER_HOST, cls.SERVER_PORT,
                                       list(settings.WS4EVER['ROUTES'].keys())[0])
        conn = create_connection(ws_url)
        gevent.sleep(0.1)
        return conn

    def test_publish_client_message(self):
        ws = self.connect()
        data = {"kind": "hello", "payload": "world"}

        notify_clients("hello", "world", a='b')
        self.assertEqual(json.loads(ws.recv()), data, "得到了message")
        ws.close()


class BroadcastCommandTest(TestCase):
    def test(self):
        backend = get_backend()

        with patch.object(backend, '_do_notify') as mock:
            call_command('broadcast', 'hello', 'world')
            self.assertTrue(mock.called, 'backend发送通知')


class ClientIndexTests(TestCase):
    def test(self):
        index = ClientIndex()

        self.assertEqual(index.get_all('a'), set())

        index.add('a', 'client1')
        self.assertEqual(index.get_all('a'), {'client1'})
        self.assertEqual(index.get_all('b'), set())

        index.add('a', 'client2')
        index.add('b', 'client3')
        self.assertEqual(index.get_all('a'), {'client1', 'client2'})
        self.assertEqual(index.get_all('b'), {'client3'})

        index.remove('a', 'client2')
        index.remove('a', 'client3')
        index.remove('b', 'client3')
        self.assertEqual(index.get_all('a'), {'client1'})
        self.assertEqual(index.get_all('b'), set())
