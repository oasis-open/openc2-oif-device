import os

from functools import partial

from sb_utils import Consumer, Producer, encode_msg, decode_msg
from .actuator import Actuator


# OnMessage Function
def on_message(act, prod, body, message):
    """
    Function that is called when a message is received from the queue/buffer
    :param act: actuator instance
    :param prod: producer to send response
    :param body: encoded message
    :param message: message instance from queue
    """
    encoding = getattr(message, "headers", {}).get('encoding', 'json')
    msg_rsp = act.action(decode_msg(body, encoding))

    prod.publish(
        headers=getattr(message, "headers", {}),
        message=encode_msg(msg_rsp, encoding),
        exchange='transport',
        routing_key=getattr(message, "headers", {}).get('transport', '').lower()
    )


if __name__ == '__main__':
    # Get dir of current file to set as root for actuator instance
    root = os.path.dirname(os.path.realpath(__file__))

    # Actuator Instance
    actuator = Actuator(root=root)

    # Begin consuming messages from internal message queue
    consumer = None
    producer = Producer(os.environ.get('QUEUE_HOST', 'localhost'), os.environ.get('QUEUE_PORT', '5672'))

    try:
        consumer = Consumer(
            exchange='actuator',
            routing_key=os.environ.get('QUEUE_ACTUATOR_KEY', actuator.profile),
            callbacks=[partial(on_message, actuator, producer)]
        )
    except Exception as e:
        print(f'Error {e}')
        consumer.shutdown()
