# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205
"""
# based on:
#  - txamqp-helpers by Dan Siemon <dan@coverfire.com> (March 2010)
#    http://git.coverfire.com/?p=txamqp-twistd.git;a=tree
#  - Post by Brian Chandler
#    https://groups.google.com/forum/#!topic/pika-python/o_deVmGondk
#  - Pika Documentation
#    https://pika.readthedocs.io/en/latest/examples/twisted_example.html
Fire up this test application via `twistd -ny twisted_service.py`
The application will answer to requests to exchange "foobar" and any of the
routing_key values: "request1", "request2", or "request3"
with messages to the same exchange, but with routing_key "response"
When a routing_key of "task" is used on the exchange "foobar",
the application can asynchronously run a maximum of 2 tasks at once
as defined by PREFETCH_COUNT
"""
import json
import pika
import requests

from dataclasses import dataclass, field
from pika.adapters import twisted_connection
from twisted.internet import defer, protocol, reactor
from typing import Callable, List, Tuple

from sb_utils import (
    ObjectDict,
    safe_json
)

PREFETCH_COUNT = 2


@dataclass
class SendMessage:
    exchange: str
    routing_key: str
    message: dict
    headers: dict = field(default_factory=dict)

    @property
    def message_bytes(self) -> bytes:
        return json.dumps(self.message).encode()


@dataclass
class ListenQueue:
    routing_key: str
    callback: Callable
    exchange: str = ""


class PikaProtocol(twisted_connection.TwistedProtocolConnection):
    """
    The protocol is created and destroyed each time a connection is created and lost
    """
    connected: bool = False
    debug: bool = False
    name: str = "Pika:AMQP:Protocol"
    factory: 'PikaFactory'
    _channel: pika.adapters.twisted_connection.TwistedChannel

    @defer.inlineCallbacks
    def connectionReady(self):
        self._channel = yield self.channel()
        yield self._channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.connected = True
        yield self._channel.confirm_delivery()
        for listener in self.factory.read_list:
            yield self.setup_read(listener)

        self.send()

    @defer.inlineCallbacks
    def read(self, listener: ListenQueue):
        """
        Add an exchange to the list of exchanges to read from
        """
        if self.connected:
            # Connection is already up. Add the reader
            self.setup_read(listener)

    # Send all messages that are queued in the factory
    def send(self):
        """
        If connected, send all waiting messages
        """
        if self.connected:
            while len(self.factory.queued_messages) > 0:
                sender = self.factory.queued_messages.pop(0)
                self.send_message(sender)

    # Do all the work that configures a listener
    @defer.inlineCallbacks
    def setup_read(self, listener: ListenQueue):
        """
        This function does the work to read from an exchange
        """
        queue = listener.routing_key  # For now use the exchange name as the queue name
        consumer_tag = listener.exchange  # Use the exchange name for the consumer tag for now

        # Declare the exchange in case it doesn't exist
        yield self._channel.exchange_declare(
            exchange=listener.exchange,
            exchange_type="topic",
            durable=True,
            auto_delete=False
        )

        # Declare the queue and bind to it
        yield self._channel.queue_declare(
            queue=queue,
            durable=True,
            exclusive=False,
            auto_delete=False
        )

        yield self._channel.queue_bind(queue=queue, exchange=listener.exchange, routing_key=listener.routing_key)

        # Consume
        (queue, _) = yield self._channel.basic_consume(queue=queue, auto_ack=False, consumer_tag=consumer_tag)

        # Now setup the readers
        self._set_queue_read(queue, listener.callback)

    def _read_item(self, item, queue, callback: Callable):
        """
        Callback function which is called when an item is read
        """
        # Setup another read of this queue
        self._set_queue_read(queue, callback)

        (channel, method_frame, header_frame, body) = item
        headers = ObjectDict(header_frame.headers)
        body = safe_json(body)

        self._log(f"{method_frame.exchange} ({method_frame.routing_key}): {body}", system=self.name)
        d = defer.maybeDeferred(callback, headers, body)
        d.addCallbacks(
            lambda _: channel.basic_ack(delivery_tag=method_frame.delivery_tag),
            lambda _: channel.basic_nack(delivery_tag=method_frame.delivery_tag)
        )

    @staticmethod
    def _read_item_err(error):
        print(error)

    @defer.inlineCallbacks
    def send_message(self, sender: SendMessage):
        """
        Send a single message
        """
        self._log(f"{sender.exchange} ({sender.routing_key}): {sender.message}", system=self.name)

        # First declare the exchange just in case it doesn't exist
        if sender.exchange:
            yield self._channel.exchange_declare(
                exchange=sender.exchange,
                exchange_type="topic",
                durable=True,
                auto_delete=False
            )

        # First declare the queue just in case it doesn't exist
        yield self._channel.queue_declare(
            queue=sender.routing_key,
            durable=True,
            auto_delete=False
        )

        try:
            yield self._channel.basic_publish(
                exchange=sender.exchange or "",
                routing_key=sender.routing_key,
                body=sender.message_bytes,
                properties=pika.spec.BasicProperties(
                    delivery_mode=2,
                    headers=sender.headers
                )
            )
        except Exception as error:  # pylint: disable=W0703
            self._log(f"Error while sending message: {error}", system=self.name)

    def _set_queue_read(self, queue, callback):
        # Now setup the readers
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)

    def _log(self, msg, **kwargs):
        if self.debug:
            pre = kwargs.pop("system") if "system" in kwargs else self.name
            pre = f"{pre} => " if pre else ""

            post = ", ".join([f"{k}: `{v}`" for k, v in kwargs.items()])
            post = f" {{{post}}}" if post else ""

            print(f"{pre}{msg}{post}")


class PikaFactory(protocol.ReconnectingClientFactory):
    name = "Pika:AMQP:Factory"
    client: PikaProtocol = None  # The protocol instance
    connected: bool = False
    protocol = PikaProtocol

    # Helper Vars
    debug: bool = False
    queued_messages: List[SendMessage]
    read_list: List[ListenQueue]

    def __init__(self, host: str = None, port: int = None, vhost: str = None, creds: Tuple[str, str] = None, debug: bool = False):
        self.host = host or 'localhost'
        self.port = port or 5672
        self.vhost = vhost or '/'
        self.creds = creds or ("guest", "guest")
        self.debug = debug

        self.queued_messages = []  # List of messages waiting to be sent
        self.read_list = []  # List of queues to listen on

        # Make the TCP connection
        reactor.connectTCP(self.host, self.port, self)  # pylint: disable=no-member

    def buildProtocol(self, addr):
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=pika.PlainCredentials(self.creds[0], self.creds[1])
        )
        p = self.protocol(parameters)
        p.factory = self  # Tell the protocol about this factory
        p.debug = self.debug  # Tell the protocol about this factory's debug status

        self.client = p  # Store the protocol

        # Reset the reconnection delay since we're connected now
        self._log("Connected", system=self.name)
        self.connected = True
        self.resetDelay()

        return p

    def startedConnecting(self, connector):
        self._log("Started to connect", system=self.name)

    def clientConnectionFailed(self, connector, reason):
        self._log(f"Connection failed. Reason: {reason.value}", system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):  # pylint: disable=W0221
        self._log(f"Lost connection.  Reason: {reason.value}", system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def send_message(self, exchange=None, routing_key=None, message=None, headers=None):
        sender = SendMessage(exchange=exchange, routing_key=routing_key, message=message, headers=headers)
        self.queued_messages.append(sender)
        if self.client is not None:
            self.client.send()

    def read_messages(self, exchange, routing_key, callback):
        """
        Configure an exchange to be read from
        """
        listen = ListenQueue(exchange=exchange, routing_key=routing_key, callback=callback)
        self.read_list.append(listen)
        if self.client is not None:
            self.client.read(listen)

    def get_exchanges(self):
        """
        Get a list of exchange names on the queue
        :return: list of exchange names
        """
        try:
            vhost = self.vhost[1:] if self.vhost.startswith("/") else self.vhost
            url = f"http://{self.host}:15672/api/exchanges/{vhost}?columns=name"
            kwargs = dict(auth=self.creds) if self.creds else {}
            response = requests.get(url, **kwargs).json()
            return list(filter(None, [que.get("name", "") for que in response]))
        except Exception:  # pylint: disable=broad-except
            return []

    def get_queues(self):
        """
        Get a list of queue names on the queue
        :return: list of queue names
        """
        try:
            vhost = self.vhost[1:] if self.vhost.startswith("/") else self.vhost
            url = f"http://{self.host}:15672/api/queues/{vhost}?columns=name"
            kwargs = dict(auth=self.creds) if self.creds else {}
            response = requests.get(url, **kwargs).json()
            return list(filter(None, [que.get("name", "") for que in response]))
        except Exception:  # pylint: disable=broad-except
            return []

    def get_binds(self):
        """
        Get a list of exchange/topic bindings
        :return: list of exchange/topic bindings
        """
        try:
            binds = []
            vhost = self.vhost[1:] if self.vhost.startswith("/") else self.vhost
            url = f"http://{self.host}:15672/api/bindings/{vhost}"
            kwargs = dict(auth=self.creds) if self.creds else {}
            response = requests.get(url, **kwargs).json()
            for queue in self.get_queues():
                for bind in response:
                    # for bind in manager.get_queue_bindings(vhost="/", qname=queue):
                    if bind.get("vhost") == self.vhost and bind.get("destination") == queue:  # and
                        binds.append({
                            "exchange": bind.get("source", ""),
                            "routing_key": bind.get("routing_key", "")
                        })
            return binds
        except Exception:  # pylint: disable=broad-except
            return []

    def _log(self, msg, **kwargs):
        if self.debug:
            pre = kwargs.pop("system") if "system" in kwargs else self.name
            pre = f"{pre} => " if pre else ""

            post = ", ".join([f"{k}: `{v}`" for k, v in kwargs.items()])
            post = f" {{{post}}}" if post else ""

            print(f"{pre}{msg}{post}")
