# amqp_tools.py
# Implements wrapper for kombu module to more-easily read/write from message queue.

import kombu  # handles interaction with AMQP server
import socket  # identify exceptions that occur with timeout
import datetime  # print time received message
import types  # determine valid functions that have been passed in
import os  # to determine localhost on a given machine
import functools
from multiprocessing import Event, Process


class Consumer(Process):
    """
    The Consumer class reads messages from message queue and determines what to do with them.
    """
    HOST = os.environ.get('QUEUE_HOST', 'localhost')
    PORT = os.environ.get('QUEUE_PORT', 5672)
    EXCHANGE = 'transport'
    ROUTING_KEY = '*'

    def __init__(self, host=HOST, port=PORT, exchange=EXCHANGE, routing_key=ROUTING_KEY, callbacks=None):
        """
        Consume message from queue exchange.
        :param host: host running RabbitMQ
        :param port: port which handles AMQP (default 5672)
        :param exchange: specifies where to read messages from
        :param routing_key:
        :param callbacks: list of callback functions which are called upon receiving a message
        """
        super().__init__()
        self.exit = Event()

        self.url = f'amqp://{host}:{port}'
        self.exchange_name = exchange

        self._callbacks = []
        self._fun_defs = (
        types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType, functools.partial)

        if type(callbacks) is list:
            for func in callbacks:
                self.add_callback(func)

        # Initialize connection we are consuming from based on defaults/passed params
        self.conn = kombu.Connection(hostname=host, port=port, userid='guest', password='guest', virtual_host='/')
        self.exchange = kombu.Exchange(self.exchange_name, type="topic")
        self.routing_key = routing_key

        # At this point, consumers are reading messages regardless of queue name
        # so I am just setting it to be the same as the exchange.
        self.queue = kombu.Queue(name=self.routing_key, exchange=self.exchange, routing_key=self.routing_key)

        # Start consumer as an independant process
        self.start()
        print("Connected to", self.url)

    def run(self):
        """
        Runs the consumer until stopped.
        :param callback: this is the function to be called. Defaults to _on_message
        """
        with kombu.Consumer(self.conn, queues=self.queue, callbacks=[self._on_message], accept=["text/plain"]):
            print(
                f'Connected to {self.url} on exchange [{self.exchange_name}], routing_key [{self.routing_key}] and waiting to consume...')
            while not self.exit.is_set():
                try:
                    self.conn.drain_events(timeout=5)
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

        print("\nMessage Received @", datetime.datetime.now())
        # print("Routing Key:", message.delivery_info.get('routing_key', ''))
        # print("Exchange:", message.delivery_info.get('exchange', ''))

        message.ack()
        for func in self._callbacks:
            func(body, message)

    def add_callback(self, fun):
        """
        Add a function to the list of callback functions.
        :param fun: function to add to callbacks
        """

        if isinstance(fun, self._fun_defs):
            if fun not in self._callbacks:
                self._callbacks.append(fun)
            else:
                raise ValueError('Duplicate function found in callbacks')

    def shutdown(self):
        """
        Shutdown the consumer and cleanly close the process
        """
        self.exit.set()
        print("The consumer has shutdown.")


class Producer(object):
    """
    The Producer class writes messages to the message queue to be consumed.
    """

    HOST = os.environ.get('QUEUE_HOST', 'localhost')
    PORT = os.environ.get('QUEUE_PORT', 5672)
    EXCHANGE = 'transport'
    ROUTING_KEY = '*'

    def __init__(self, host=HOST, port=PORT):
        """
        Sets up connection to broker to write to.
        :param host: hostname for the queue server
        :param port: port for the queue server
        """
        self.url = f'amqp://{host}:{port}'
        self._conn = kombu.Connection(hostname=host, port=port, userid='guest', password='guest', virtual_host='/')

    def publish(self, message="", header={}, exchange=EXCHANGE, routing_key=ROUTING_KEY):
        """
        Publish a message to th AMQP Queue
        :param message: message to be published
        :param header: header key-values to publish with the message
        :param exchange: specifies the top level specifier for message publish
        :param routing_key: determines which queue the message is published to
        """
        self._conn.connect()
        queue = kombu.Queue(routing_key, kombu.Exchange(exchange, type='topic'), routing_key=routing_key)
        queue.maybe_bind(self._conn)
        queue.declare()

        producer = kombu.Producer(self._conn.channel())
        producer.publish(
            message,
            headers=header,
            exchange=queue.exchange,
            routing_key=queue.routing_key,
            declare=[queue]
        )
        print("Sent:\n", str(message))
        producer.close()
        self._conn.release()
