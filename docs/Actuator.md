# Adding your own actuator to O.I.F.

This is a tutorial on how to allow your device to receive messages from the O.I.F. Orchestrator. In order to add the Actuator on the GUI side, read the section of [ReadMe.md](ReadMe.md) titled <i>Registering an actuator with the OIF</i>

### <b>Add Actuator to Docker Stack</b>

Open the [Device Compose file](device-compose.yaml) to add your actuator to the stack. You can copy-paste the actuator-isr image and replace it with your actuator's info. Read more on Docker Compose [here](https://docs.docker.com/compose/overview/).

Here is what our actuator looks like:

```yaml
actuator-isr:                                   # container name
    hostname: actuator-isr                      # hostname of container 
    image: O.I.F./actuator:isr                     # image name
    build:
      context: ./device/isr                     # location of Dockerfile
    env_file:
    - ./environment/queue.connect.env           # path to shared environment variables
    environment:
      QUEUE_EXCHANGE: 'actuator'                # actuator specific environment variable (this can stay the same for your container)
    external_links:
      - queue                                   # link to internal buffer (more on this below)
    depends_on:
      - queue                                   # indicates that this container should wait for queue to exist before running
    entrypoint:                                 # indicates script to run upon container startup
      - sh
      - start.sh
    restart: on-failure:5                       # if fail to start - retries maximum of 5 times
```

Once added to device-compose.yaml, your actuator will be brought up as a part of the docker compose stack and be added to the stack's docker network.

### <b>Receiving a command</b>

The O.I.F. Orchestrator and included test Actuator each utilize an internal buffer. This buffer is a structure that is a part of the O.I.F. for routing messages to the correct locations, but NOT a part of OpenC2 itself. This "buffer", as we refer to it, is simply an AMQP implementation that listens for incoming commands from a Transport Module which routes the OpenC2 Command to the desired actuator.

The path that the message follows is:

Orchestrator (you create the command here) -> Buffer -> Transport -> Device-side Transport -> Device-side buffer -> Actuator (this is where your actuator will live)

You may want to copy our wrapper for the AMQP library, [Kombu](https://kombu.readthedocs.io/en/latest/), as well as other utilities. View the libraries here: [utils](device/isr/act_server/utils), [actuator](device/isr/act_server/actuator)
```python
from .utils import decode_msg, encode_msg, FrozenDict, MessageQueue, safe_cast
from .actuator import Actuator  # contains basic actuator methods and actuator data
```

To hook your actuator up to the buffer you will need to add some code to connect to the AMQP broker (we use RabbitMQ), which is included with the Device's Docker Compose file. You can find an example from the test [ISR Actuator](device/isr/act_server/__main__.py).  

The code needed looks like this:

```python
CONFIG = FrozenDict(dict(
        hostname=os.environ.get('QUEUE_HOST', 'localhost'),
        port=safe_cast(os.environ.get('QUEUE_PORT', 5672), int),
        auth=dict(
            username=os.environ.get('QUEUE_USER', 'guest'),
            password=os.environ.get('QUEUE_PASSWORD', 'guest')
        ),
        exchange=os.environ.get('QUEUE_EXCHANGE', 'actuator'),
        consumer_key=os.environ.get('QUEUE_ACTUATOR_KEY', actuator.schema.profiles)
    ))

    msgQueue = MessageQueue(**CONFIG, callbacks=[partial(on_message, actuator)])
```

The environment variables `QUEUE_HOST`, `QUEUE_PORT`, `QUEUE_USER`, and `QUEUE_PASSWORD` are set in [queue.connect.env](environment/queue.connect.env). The default values will allow you to connect to the included RabbitMQ broker, which does not expose its port outside of its Docker Network (e.g. all containers within the [device-compose.yaml](device-compose.yaml)).

The values `QUEUE_EXCHANGE` default is `actuator` and `QUEUE_ACTUATOR_KEY` is the actuator profile name, for the ISR actuator it is `ISR_Actuator_Profile`, but you can pull that information from the schema. The Transport Module which you utilize will be expecting your actuator to be listening on this exchange and routing key. Click [here](https://www.rabbitmq.com/tutorials/amqp-concepts.html) to learn more about the AMQP Model.

### <b>Processing the Command and sending Response</b>

At this point, if set up properly, your actuator should be able to retrieve a message that the device side transport has placed onto the specified exchange and routing key.

When the actuator receives a message from the queue, it triggers a callback method. This callback method is in charge of passing the command for your actuator to process, and then send out the processed response. You can see our example in the same file location as the above code [here](device/isr/act_server/__main__.py).

It looks like this:

```python
def on_message(act, que, body, message):
    '''
    Callback method triggered upon receiving message from AMQP broker
    :param act: method passed to callback to be triggered, will be the link from callback to actuator
    :param que: MessageQueue object which handles sending the response
    :param body: message body, ie. the OpenC2 Command
    :param message: contains info about the message as well as headers 
    '''
    encoding = getattr(message, "headers", {}).get('encoding', 'json')  # retrieve encoding specified in headers
    msg_rsp = act.action(decode_msg(body, encoding))                    # deserialize and give message to actuator and get response

    # send response back to the device transport to route back to the orchestrator
    que.send(  
        msg=encode_msg(msg_rsp, encoding),
        header=getattr(message, "headers", {}),
        routing_key=getattr(message, "headers", {}).get('transport', '').lower(),
        exchange='transport',
    )
```

What you may want to replace here is the line ```msg_rsp = act.action(decode_msg(body, encoding))``` and replace ```act.action( ... )``` with the action/handling that is contained within your actuator. 

If all is successful, your actuator will now be able to receive a command from the buffer, process it, and send back the response.

