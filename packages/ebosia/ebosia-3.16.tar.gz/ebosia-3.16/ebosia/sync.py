import logging
import time
from enum import Enum

from kombu import Connection, Consumer, Exchange, Queue
from kombu.pools import producers
from kombu.utils import nested

import ebosia
import ebosia.connection
import ebosia.events

LOGGER = logging.getLogger(__name__)

def errback(exc, interval):
    LOGGER.warning("Failed to publish message: %s. Retrying publish in %s seconds", exc, interval)

class ConnectionSync(ebosia.connection.ConnectionBase):
    def __init__(self, uri, timeout=None):
        self.consumers = []
        self.timeout = timeout
        self._connection = Connection(uri)
        to_wait = 1.5
        time_waited = 0
        while True:
            try:
                self._connection.connect()
                break
            except OSError as e:
                to_wait = round(min(30, (to_wait ** 1.5)), 2)
                LOGGER.info("Failed to connect to RabbitMQ: %s. Waiting %s seconds to see if RabbitMQ at %s comes online...",
                    e, to_wait, uri)
                time.sleep(to_wait)
                time_waited += to_wait
        if time_waited:
            LOGGER.info("Waited a total of %s seconds for RabbitMQ to come online", time_waited)

    def publish(self, topic, payload):
        LOGGER.debug("Publishing %s %s", topic, payload)
        exchange = Exchange('eventbus', type='topic')
        with producers[self._connection].acquire(block=True) as producer:
            _publish = self._connection.ensure(producer, producer.publish, errback=errback, max_retries=3)
            result = _publish(
                ebosia.events.safe_to_serialize(payload),
                serializer  = 'json',
                compression = 'bzip2',
                exchange    = exchange,
                routing_key = topic if not isinstance(topic, Enum) else str(topic),
            )
            LOGGER.info("Published %s %s with result %s", topic, payload, result)
            return result

    def subscribe(self, routing_key, callback):
        def _on_message(body, message):
            event = ebosia.events.from_kombu(body, message)
            callback(event)
        exchange = Exchange('eventbus', type='topic', durable=False)
        queue = Queue('', exchange, routing_key=routing_key)
        consumer = Consumer(self._connection, [queue], callbacks=[_on_message])
        self.consumers.append(consumer)

    def drain(self):
        with nested(*self.consumers):
            self._connection.drain_events(timeout=self.timeout)

def connect(uri):
    connection = ConnectionSync(uri)
    ebosia.store(connection)
    return connection

def publish(topic, payload, bus=None):
    bus = bus or ebosia.get()
    return bus.publish(topic, payload)

def subscribe(routing_key, callback, bus=None):
    bus = bus or ebosia.get()
    return bus.subscribe(routing_key, callback)

def drain(bus=None):
    bus = bus or ebosia.get()
    return bus.drain()
