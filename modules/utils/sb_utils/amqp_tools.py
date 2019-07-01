"""
amqp_tools.py
Implements wrapper for kombu module to more-easily read/write from message queue.
"""
import kombu  # handles interaction with AMQP server
import socket  # identify exceptions that occur with timeout
import datetime  # print time received message
import os  # to determine localhost on a given machine

from functools import partial
from inspect import isfunction
from multiprocessing import Event, Process
from typing import Union


class Consumer(Process):
    """
    The Consumer class reads messages from message queue and determines what to do with them.
    """
    HOST = os.environ.get("QUEUE_HOST", "localhost")
    PORT = os.environ.get("QUEUE_PORT", 5672)
    EXCHANGE = "transport"
    ROUTING_KEY = "*"

    def __init__(self, host: str = HOST, port: int = PORT, exchange: str = EXCHANGE, routing_key: str = ROUTING_KEY, callbacks: Union[list, tuple] = None, debug: bool = False):
        """
        Consume message from queue exchange.
        :param host: host running RabbitMQ
        :param port: port which handles AMQP (default 5672)
        :param exchange: specifies where to read messages from
        :param routing_key:
        :param callbacks: list of callback functions which are called upon receiving a message
        :param debug: print debugging messages
        """
        super().__init__()
        self._exit = Event()

        self._url = f"amqp://{host}:{port}"
        self._exchange_name = exchange
        self._callbacks = ()
        self._debug = debug

        if isinstance(callbacks, (list, tuple)):
            for func in callbacks:
                self.add_callback(func)

        # Initialize connection we are consuming from based on defaults/passed params
        self._conn = kombu.Connection(hostname=host, port=port, userid="guest", password="guest", virtual_host="/")
        self._exchange = kombu.Exchange(self._exchange_name, type="topic")
        self._routing_key = routing_key

        # At this point, consumers are reading messages regardless of queue name
        # so I am just setting it to be the same as the exchange.
        self._queue = kombu.Queue(name=self._routing_key, exchange=self._exchange, routing_key=self._routing_key)

        # Start consumer as an independent process
        self.start()
        if self._debug:
            print(f"Connected to {self._url}")

    def run(self) -> None:
        """
        Runs the consumer until stopped.
        """
        with kombu.Consumer(self._conn, queues=self._queue, callbacks=[self._on_message], accept=["text/plain", "application/json"]):
            if self._debug:
                print(f"Connected to {self._url} on exchange [{self._exchange_name}], routing_key [{self._routing_key}] and waiting to consume...")

            while not self._exit.is_set():
                try:
                    self._conn.drain_events(timeout=5)
                except socket.timeout:
                    pass
                except KeyboardInterrupt:
                    self.shutdown()

    def _on_message(self, body, message):
        """
        Default option for a consumer callback, prints out message and message data.
        :param body: contains the body of the message sent
        :param message: contains meta data about the message sent (ie. delivery_info)
        """
        if self._debug:
            print(f"Message Received @ {datetime.datetime.now()}")

        message.ack()
        for func in self._callbacks:
            func(body, message)

    def add_callback(self, fun):
        """
        Add a function to the list of callback functions.
        :param fun: function to add to callbacks
        """
        if isfunction(fun) or isinstance(fun, partial):
            if fun in self._callbacks:
                raise ValueError("Duplicate function found in callbacks")
            self._callbacks = (*self._callbacks, fun)

    def get_exchanges(self):
        """
        Get a list of exchange names on the queue
        :return: list of exchange names
        """
        exchanges = self._conn.get_manager().get_exchanges()
        return list(filter(None, [exc.get("name", "")for exc in exchanges]))

    def get_queues(self):
        """
        Get a list of queue names on the queue
        :return: list of queue names
        """
        queues = self._conn.get_manager().get_queues()
        return list(filter(None, [que.get("name", "") for que in queues]))

    def get_binds(self):
        """
        Get a list of exchange/topic bindings
        :return: list of exchange/topic bindings
        """
        binds = []
        manager = self._conn.get_manager()
        for queue in self.get_queues():
            for bind in manager.get_queue_bindings(vhost="/", qname=queue):
                binds.append({
                    "exchange": bind.get("source", ""),
                    "routing_key": bind.get("routing_key", "")
                })

        return binds

    def shutdown(self):
        """
        Shutdown the consumer and cleanly close the process
        """
        self._exit.set()
        print("The consumer has shutdown.")


class Producer(object):
    """
    The Producer class writes messages to the message queue to be consumed.
    """
    HOST = os.environ.get("QUEUE_HOST", "localhost")
    PORT = os.environ.get("QUEUE_PORT", 5672)
    EXCHANGE = "transport"
    ROUTING_KEY = "*"

    def __init__(self, host: str = HOST, port: int = PORT, debug: bool = False):
        """
        Sets up connection to broker to write to.
        :param host: hostname for the queue server
        :param port: port for the queue server
        :param debug: print debugging messages
        """
        self._url = f"amqp://{host}:{port}"
        self._debug = debug
        self._conn = kombu.Connection(hostname=host, port=port, userid="guest", password="guest", virtual_host="/")

    def publish(self, message: Union[dict, str] = "", headers: dict = {}, exchange: str = EXCHANGE, routing_key: str = ROUTING_KEY):
        """
        Publish a message to th AMQP Queue
        :param message: message to be published
        :param headers: header key-values to publish with the message
        :param exchange: specifies the top level specifier for message publish
        :param routing_key: determines which queue the message is published to
        """
        self._conn.connect()
        queue = kombu.Queue(routing_key, kombu.Exchange(exchange, type="topic"), routing_key=routing_key)
        queue.maybe_bind(self._conn)
        queue.declare()

        producer = kombu.Producer(self._conn.channel())
        producer.publish(
            message,
            headers=headers,
            exchange=queue.exchange,
            routing_key=queue.routing_key,
            declare=[queue]
        )
        producer.close()
        self._conn.release()
