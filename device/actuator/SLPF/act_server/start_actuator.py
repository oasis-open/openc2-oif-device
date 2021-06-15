import os
import signal
import sys

from functools import partial
from sb_utils import decode_msg, encode_msg, Consumer, Producer

from actuator import Actuator

# Signals
signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
}


# OnMessage Function
def on_message(act: Actuator, prod: Producer, body, message):
    """
    Function that is called when a message is received from the queue/buffer
    :param act: actuator instance
    :param prod: producer to send response
    :param body: encoded message
    :param message: message instance from queue
    """
    headers = getattr(message, "headers", {})
    headers.setdefault("profile", act.profile)
    msg_id = headers.get('correlationID', '')
    encoding = headers.get('encoding', 'json')
    msg = decode_msg(body, encoding)
    msg_rsp = act.action(msg_id=msg_id, msg=msg)
    print(f"{act} -> received: {msg}")
    print(f"{act} -> response: {msg_rsp}")

    if msg_rsp:
        prod.publish(
            headers=headers,
            message=encode_msg(msg_rsp, encoding),
            exchange='transport',
            routing_key=headers.get('transport', '').lower()
        )


def on_exit(signum, stack):
    print(f'Received {signals[signum]} signal')
    consumer.shutdown()
    actuator.shutdown()
    sys.exit(signum)


if __name__ == '__main__':
    # Get dir of current file to set as root for actuator instance
    root = os.path.dirname(os.path.realpath(__file__))

    # Actuator Instance
    actuator = Actuator(root=root)

    # Actuator nsid/profile
    queue = actuator.nsid if len(actuator.nsid) > 0 else [actuator.profile]

    # Begin consuming messages from internal message queue
    consumer = None
    producer = Producer(os.environ.get('QUEUE_HOST', 'localhost'), os.environ.get('QUEUE_PORT', '5672'))

    # Set Queue Bindings
    bindings = {}
    for q in queue:
        bindings[q] = [
            'actuator',
            ('actuator_all', 'fanout', 'actuator_all')
        ]

    try:
        consumer = Consumer(
            exchange='actuator',
            # TODO: Get NSID??
            binding=bindings,
            callbacks=[partial(on_message, actuator, producer)]
        )
    except Exception as e:
        print(f'Error {e}')
        consumer.shutdown()

    for sig in signals:
        signal.signal(sig, on_exit)
