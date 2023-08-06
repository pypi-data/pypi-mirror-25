import bz2
import collections
import datetime
import json

Event = collections.namedtuple('Event', ['topic', 'payload'])

def from_kombu(body, message):
    #topic = message.properties['delivery_info'].get('routing_key')
    topic = message.delivery_info['routing_key']
    return Event(topic, body)

def from_aioamqp(body, envelope, properties): # pylint: disable=unused-argument
    decompressed = bz2.decompress(body)
    decoded = decompressed.decode('utf-8')
    parsed = json.loads(decoded)
    topic = envelope.routing_key
    return Event(topic, parsed)

def safe_to_serialize(payload):
    if isinstance(payload, dict):
        return {k: safe_to_serialize(v) for k, v in payload.items()}
    elif isinstance(payload, (tuple, set, list)):
        return [safe_to_serialize(v) for v in payload]
    elif isinstance(payload, (int, float)):
        return payload
    elif isinstance(payload, datetime.datetime):
        return payload.isoformat()
    elif isinstance(payload, type(None)):
        return payload
    else:
        return str(payload)
