from sb_utils import Consumer, FrozenDict, safe_cast, Producer


class MessageQueue(object):
    AUTH = FrozenDict({
        'username': 'guest',
        'password': 'guest'
    })
    EXCHANGE = 'orchestrator'
    CONSUMER_KEY = 'response'
    PRODUCER_EXCHANGE = 'transport'

    def __init__(self, hostname='127.0.0.1', port=5672, auth=AUTH, exchange=EXCHANGE, consumer_key=CONSUMER_KEY, producer_exchange=PRODUCER_EXCHANGE, callbacks=None):
        """
        Message Queue - holds a consumer class and producer class for ease of use
        :param hostname: server ip/hostname to connect
        :param port: port the AMQP Queue is listening
        :param auth: dict of username/password for connection auth
        :param exchange: name of the default exchange
        :param consumer_key: key to consumer
        :param callbacks: list of functions to call on message receive
        """
        if self.EXCHANGE != exchange:
            self.EXCHANGE = exchange

        if self.PRODUCER_EXCHANGE != producer_exchange:
            self.PRODUCER_EXCHANGE = producer_exchange

        self._publish_opts = dict(
            host=hostname,
            port=safe_cast(port, int)
        )

        self._consume_opts = dict(
            host=hostname,
            port=safe_cast(port, int),
            exchange=exchange,
            routing_key=consumer_key,
            callbacks=callbacks
        )

        self.producer = Producer(**self._publish_opts)
        self.consumer = Consumer(**self._consume_opts)

    def send(self, msg, headers={}, exchange=PRODUCER_EXCHANGE, routing_key=None):
        """
        Publish a message to the specified que and transport
        :param msg: message to be published
        :param header: header information for the message being sent
        :param exchange: exchange name
        :param routing_key: routing key name
        """
        if routing_key is None:
            print('Sending Message')
            raise ValueError('Routing Key cannot be None')
        else:
            print('Sending Message')
            self.producer.publish(
                message=msg,
                headers=headers,
                exchange=exchange,
                routing_key=routing_key
            )

    def register_callback(self, fun):
        """
        Register a function for when a message is received from the message queue
        :param fun: function to register
        """
        self.consumer.add_callback(fun)

    def shutdown(self):
        """
        Shutdown the queue
        """
        self.consumer.shutdown()
        self.consumer.join()
        print('MessageQueue Shutdown')
