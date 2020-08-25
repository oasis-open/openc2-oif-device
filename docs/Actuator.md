# Adding your own actuator to O.I.F.

This is a tutorial on how to allow your device to receive messages from the O.I.F. Orchestrator. In order to add the Actuator on the GUI side, read the section of [Device](./Device.md#Registration) titled __Registration__

### Add an Actuator to the Docker Stack

Open the [Device Compose file](../device-compose.yaml) to add your actuator to the stack. You can copy and edit the actuator-slpf image and replace it with your actuator's info. Read more on Docker Compose [here](https://docs.docker.com/compose/overview/).

Here is what our actuator looks like:

```yaml
actuator-slpf:                              # container name
    hostname: actuator-slpf                 # hostname of container 
    image: g2inc/oif-device-actutator-isr   # image name
    build:
      context: ./device/slpf                # location of Dockerfile
    env_file:
    - ./environment/queue.connect.env       # path to shared environment variables
    environment:
      QUEUE_EXCHANGE: 'actuator'            # actuator specific environment variable (this can stay the same for your container)
    external_links:
      - queue                               # link to internal buffer (more on this below)
    depends_on:
      - queue                               # indicates that this container should wait for queue to exist before running
    restart: on-failure:5                   # if fail to start - retries maximum of 5 times
```

Once added to device-compose.yaml, your actuator will be brought up as a part of the docker compose stack and be added to the stack's docker network.

### Receiving a command

The O.I.F. Orchestrator and included test Actuator each utilize an internal buffer. This buffer is a structure that is a part of the O.I.F. for routing messages to the correct locations, but NOT a part of OpenC2 itself. This "buffer", as we refer to it, is simply an AMQP implementation that listens for incoming commands from a Transport Module which routes the OpenC2 Command to the desired actuator.

The path that the message follows is:

Orchestrator (you create the command here) -> Buffer -> Transport -> Device-side Transport -> Device-side buffer -> Actuator (this is where your actuator will live)

You may want to copy our wrapper for the AMQP library, [Kombu](https://kombu.readthedocs.io/en/latest/), as well as other utilities.
- [SB_Utils](../base/modules/utils)
    - Contains two packages, root is the primary package and actuator is the supporting actuator base options
    - To use the actuator package, the root package should be installed first

To connect your actuator to the buffer you will need to add some code to connect to the AMQP broker (we use RabbitMQ), which is included with the Device's Docker Compose file. You can find an example from the test [ISR Actuator](../device/isr/act_server/__main__.py).  

The code needed will look similar to the following:

```python
import os
from functools import partial
from sb_utils import decode_msg, encode_msg, safe_cast, Consumer, FrozenDict, Producer
from .actuator import Actuator

if __name__ == "__main__":
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
```

The environment variables `QUEUE_HOST`, `QUEUE_PORT` are set in [queue.connect.env](environment/queue.connect.env). The default values will allow you to connect to the included RabbitMQ broker, which does not expose its port outside of its Docker Network (e.g. all containers within the [device-compose.yaml](../device-compose.yaml)).

The value `QUEUE_ACTUATOR_KEY` is the actuator profile name, for the ISR actuator it is `ISR_Actuator_Profile`, you can pull this information from the actuator's schema. The Transport Module which you utilize will be expecting your actuator to be listening on this exchange and routing key. Click [here](https://www.rabbitmq.com/tutorials/amqp-concepts.html) to learn more about the AMQP Model.

### Processing the Command and sending Response

At this point, if set up properly, your actuator should be able to retrieve a message that the device side transport has placed onto the specified exchange and routing key.

When the actuator receives a message from the queue, it triggers a callback method. This callback method is in charge of passing the command for your actuator to process, and then send out the processed response. You can see our example in the same file location as the above code [here](../device/isr/act_server/__main__.py).

It looks similar to the following:

```python
from sb_utils import decode_msg, encode_msg
# OnMessage Function
def on_message(act, prod, body, message):
    """
    Function that is called when a message is received from the queue/buffer
    :param act: actuator instance
    :param prod: producer to send response
    :param body: encoded message
    :param message: message instance from queue
    """
    headers = getattr(message, "headers", {})
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
```

What you may want to replace here is the line ```msg_rsp = act.action( ... )``` with the action/handling  function that is contained within your actuator. 

If all is successful, your actuator will now be able to receive a command from the buffer, process it, and send back the response.

