import collections

import pytest

import ebosia as _ebosia
from ebosia import sync


class TestConnection(sync.ConnectionSync):
    PRETENDING_TO_BE_ASYNC = True
    def __init__(self):
        super().__init__('memory:///', 0.1)
        self.events         = collections.deque()
        self.consumer       = super().subscribe('#', self.process)
        self.subscriptions  = []

    def process(self, event):
        self.events.append(event)
        for topic, callback in self.subscriptions:
            if topic == '#' or event.topic == topic:
                callback(event)

    def publish(self, topic, payload):
        super().publish(topic, payload)
        self.drain()

    def published(self, topic, payload=None):
        if len(self.events) < 1:
            return False
        event = self.events.popleft()
        if payload is None:
            assert event.topic == topic
            return event.topic == topic
        else:
            assert event.topic == topic and event.payload == payload
            return event.topic == topic and event.payload == payload

    def subscribe(self, topic, callback):
        self.subscriptions.append((topic, callback))

@pytest.yield_fixture
def eventbus_connection():
    previous = None
    try:
        previous = _ebosia.get()
    except Exception: # pylint: disable=broad-except
        pass
    connection = TestConnection()
    _ebosia.store(connection)
    yield connection
    _ebosia.store(previous)

@pytest.yield_fixture
def eventbus(eventbus_connection): # pylint: disable=redefined-outer-name
    yield eventbus_connection
