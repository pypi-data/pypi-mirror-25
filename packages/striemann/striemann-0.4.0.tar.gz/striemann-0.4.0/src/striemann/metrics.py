__all__ = [
    'MetricId',
    'Recorder',
    'LogTransport',
    'InMemoryTransport',
    'RiemannTransport',
    'CompositeTransport',
    'Gauge',
    'Counter',
    'Timer',
    'Metrics',
]


from collections import defaultdict, namedtuple
import collections
import json
import logging
import socket
import timeit

from ._deprecation import deprecated

from riemann_client.client import Client
from riemann_client.riemann_pb2 import Msg
from riemann_client.transport import TCPTransport


MetricId = namedtuple('MetricId', ['name', 'tags', 'attributes'])

class Metric:

    def __init__(self, service, value, ttl, tags, fields):
        self.id = self._id(service, tags, fields)
        self.value = value
        self.name = service
        self.tags = tags
        self.ttl = ttl
        self.attributes = {str(k): str(v) for k, v in fields.items()}

    def _id(self, service_name, tags, fields):
        return MetricId(
            service_name, frozenset(tags), frozenset(fields.items())
        )


class Recorder:
    """
    Base type for recorders - objects that forward metrics over a transport
    """
    def send(self, metric, value, transport, suffix=""):
        ttl = metric.ttl
        event = {
            "tags": metric.tags,
            "attributes": metric.attributes,
            "service": metric.name + suffix,
            "metric_f": value
        }
        if not ttl is None:
            event['ttl'] = ttl

        transport.send_event(event)


class LogTransport:

    """
    Simple Transport that sprints metrics to the log. Useful for development
    environments
    """
    def __init__(self):
        self._logger = logging.getLogger("metrics")

    def send_event(self, event):
        self._logger.info(
            "metric %s=%s (%s)",
            event['service'],
            event['metric_f'],
            json.dumps(event.get('attributes'))
        )

    def flush(self, is_closing):
        pass


class InMemoryTransport:

    """
    Dummy transport that keeps a copy of the last flushed batch of events. This
    is used to store the data for the stats endpoints.
    """
    def __init__(self):
        self.current_batch = []
        self.last_batch = []

    def send_event(self, event):
        self.current_batch.append(event)

    def flush(self, is_closing):
        self.last_batch = list(self.current_batch)
        self.current_batch = []


class RiemannTransport:

    """
    Transport that sends metrics to a Riemann server.
    """

    def __init__(self, host="localhost", port="5555", timeout=5):
        self.host = host
        self.port = port

        self.transport = TCPTransport(self.host, self.port, timeout)
        self._new_message()
        self._connected = False

    def send_event(self, event):
        riemann_event = Client.create_event(event)
        self._message.events.add().MergeFrom(riemann_event)

    def _ensure_connected(self):
        # This is just to avoid logging about failure on the first try
        if not self._connected:
            self.transport.connect()
            self._connected = True

    def flush(self, is_closing):
        self._ensure_connected()
        try:
            self.transport.send(self._message)
        except Exception as e:
            self.transport.disconnect()
            logging.warning("Failed to flush metrics to riemann")
            self.transport.connect()
            try:
                self.transport.send(self._message)
            except Exception as e:
                logging.error(
                    "Failed twice to flush metrics to riemann", exc_info=True
                )
        if is_closing:
            self.transport.disconnect()
        self._new_message()

    def _new_message(self):
        self._message = Msg()

    @deprecated("Should be no need to check, will reconnect automatically")
    def is_connected(self):
        """Check whether the transport is connected."""
        return True


class CompositeTransport:

    """
    Transport that wraps two or more transports and forwards events to all of
    them.
    """

    def __init__(self, *args):
        self.transports = args

    def send_event(self, event):
        for t in self.transports:
            t.send_event(event)

    def flush(self, is_closing):
        for t in self.transports:
            t.flush(is_closing)


class Gauge(Recorder):
    """
    Gauges record a scalar value at a point in time. For example: response
    time, number of active sessions, disk space free
    """

    def __init__(self, source):
        self.source = source
        self.reset()

    def reset(self):
        self.gauges = defaultdict(list)

    def record(self, service_name, value, ttl=None, tags=[], attributes=dict()):
        if self.source:
            attributes['source'] = self.source
        metric = Metric(service_name, value, ttl, tags, attributes)
        self.gauges[metric.id].append(metric)

    def flush(self, transport):
        for gauge in self.gauges.values():

            first = gauge[0]
            _min = first.value
            _max = first.value
            _mean = 0
            _count = 0
            _total = 0

            for measurement in gauge:
                _count = _count + 1
                _total = _total + measurement.value
                _max = max(_max, measurement.value)
                _min = min(_min, measurement.value)

            _mean = (_total / _count)

            self.send(first, _min, transport, ".min")
            self.send(first, _max, transport, ".max")
            self.send(first, _mean, transport, ".mean")
            self.send(first, _count, transport, ".count")

        self.reset()


class Counter(Recorder):

    """
    Counters record incrementing or decrementing values, eg. Events Processed,
    error count, cache hits.
    """
    def __init__(self, source):
        self.source = source
        self.counters = collections.defaultdict(list)

    def record(self, service_name, value, ttl, tags, attributes):
        if self.source:
            attributes['source'] = self.source
        metric = Metric(service_name, value, ttl, tags, attributes)

        self.counters[metric.id].append(metric)

    def flush(self, transport):
        for counter in self.counters.values():
            count = sum(m.value for m in counter)
            self.send(counter[0], count, transport)
        self.counters = defaultdict(list)


class Timer:

    """
    Timers provide a context manager that times an operation and records a
    gauge with the elapsed time.
    """
    def __init__(self, service_name, ttl, tags, attributes, gauge):
        self.service_name = service_name
        self.ttl = ttl
        self.tags = tags
        self.attributes = attributes
        self.recorder = gauge

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        elapsed = timeit.default_timer() - self.start
        self.recorder.record(
            self.service_name, elapsed, self.ttl, self.tags, self.attributes
        )


class Metrics:

    def __init__(self, transport, source=None):
        self.transport = transport
        self.gauges = Gauge(source)
        self.counters = Counter(source)

    def recordGauge(self, service_name, value, ttl=None,tags=[], **kwargs):
        self.gauges.record(service_name, value, ttl, tags, kwargs)

    def incrementCounter(self, service_name, value=1, ttl=None,tags=[], **kwargs):
        self.counters.record(service_name, value, ttl, tags, kwargs)

    def decrementCounter(self, service_name, value=1, ttl=None,tags=[], **kwargs):
        self.counters.record(service_name, 0 - value, ttl, tags, kwargs)

    def time(self, service_name, ttl=None, tags=[], **kwargs):
        return Timer(service_name, ttl, tags, kwargs, self.gauges)

    def flush(self, is_closing=False):
        self.gauges.flush(self.transport)
        self.counters.flush(self.transport)
        self.transport.flush(is_closing)
