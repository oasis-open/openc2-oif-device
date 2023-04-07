# callbacks.py
import json
import logging
import os
import ssl
import uuid

from typing import List
from paho.mqtt import MQTTException, client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
from paho.mqtt.subscribeoptions import SubscribeOptions
from sb_utils import FrozenDict, Message, MessageType, Producer, SerialFormats, safe_cast
from config import Config

# Constants .
SUBSCRIBE_OPTIONS = SubscribeOptions(
    qos=1,
    noLocal=True,
    retainAsPublished=True,
    retainHandling=SubscribeOptions.RETAIN_SEND_ON_SUBSCRIBE
)
RequiredHeaderKeys = {"encoding", "orchestratorID", "socket"}


# Helper Functions
def send_error_response(e, header):
    """
    If error occurs before leaving the transport on the orchestrator side, then send back a message
    response to the internal buffer indicating so.
    :param e: Exception thrown
    :param header: Include headers which would have been sent for Orchestrator to read.
    """
    producer = Producer(
        os.environ.get("QUEUE_HOST", "localhost"),
        os.environ.get("QUEUE_PORT", "5672")
    )

    err = json.dumps(str(e))
    print(f"Send error response: {err}")

    producer.publish(
        headers=header,
        message=err,
        exchange="orchestrator",
        routing_key="response"
    )


# MQTT single publish functions
def _do_publish(client: mqtt.Client, userdata: List[dict]):
    if len(userdata) > 0:
        message = userdata.pop()
        if isinstance(message, dict):
            client.publish(**message)
        elif isinstance(message, (tuple, list)):
            client.publish(*message)
        else:
            raise TypeError("message must be a dict, tuple, or list")


def _on_connect(client: mqtt.Client, userdata: List[dict], flags: dict, rc: int, props: Properties = None):
    # pylint: disable=invalid-name, unused-argument
    if rc == 0:
        if len(userdata) > 0:
            _do_publish(client, userdata)
    else:
        raise MQTTException(mqtt.connack_string(rc))


def _on_publish(client: mqtt.Client, userdata: List[dict], mid: int):
    # pylint: disable=unused-argument
    if len(userdata) == 0:
        client.disconnect()
    else:
        _do_publish(client, userdata)


def publish_single(config: FrozenDict, topic, payload, client_id="", properties: Properties = None):
    client = mqtt.Client(
        client_id=client_id,
        userdata=[
            {"topic": topic, "payload": payload, "qos": 1, "retain": False, "properties": properties}
        ],
        protocol=mqtt.MQTTv5,
        transport="tcp"
    )

    # set auth
    if config.USERNAME:
        client.username_pw_set(
            username=config.USERNAME,
            password=config.PASSWORD
        )

    # check that certs exist
    if config.TLS_ENABLED:
        client.tls_insecure_set(safe_cast(config.TLS_SELF_SIGNED, bool, False))
        client.tls_set(
            ca_certs=config.CAFILE,
            certfile=config.CLIENT_CERT,
            keyfile=config.CLIENT_KEY,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )

    # set callbacks
    client.on_connect = _on_connect
    client.on_publish = _on_publish

    client.connect(
        host=config.MQTT_HOST,
        port=config.MQTT_PORT,
        keepalive=300,
        clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY
    )
    client.loop_forever()


def send_mqtt(config: FrozenDict, body, message):
    """
    AMQP Callback when we receive a message from internal buffer to be published to MQTT Broker
    :param config: MQTT connection information
    :param body: Contains the message to be sent.
    :param message: Contains data about the message as well as headers
    """
    headers = message.headers
    broker_socket = headers.get("socket", "localhost:1883")
    encoding = headers.get("encoding", "json")
    orc_id = headers.get("orchestratorID", "")
    topic = "/".join(filter(None, [Config.MQTT_PREFIX, "oc2", "rsp"]))
    if Config.RSP_SPECIFIC:
        topic += f"/{orc_id}"

    print(f"Preparing {topic} for data: {body}")
    # build message for MQTT
    payload = Message(
        recipients=f"{orc_id}@{broker_socket}",
        origin=f"{headers.get('profile', '')}@{broker_socket}",
        # created: datetime = None,
        msg_type=MessageType.Response,
        request_id=uuid.UUID(headers.get("correlationID", "")),
        content_type=SerialFormats(encoding) if encoding in SerialFormats else SerialFormats.JSON,
        content=body if isinstance(body, dict) else json.loads(body)
    )
    # Transport is running on device side, send response to orchestrator
    key_diff = RequiredHeaderKeys.difference({*headers.keys()})
    if len(key_diff) == 0:
        publish_props = Properties(PacketTypes.PUBLISH)
        publish_props.PayloadFormatIndicator = 1
        publish_props.ContentType = "application/openc2"
        publish_props.UserProperty = ("msgType", payload.msg_type)
        publish_props.UserProperty = ("encoding", payload.content_type)

        try:
            publish_single(
                config=config,
                topic=topic,
                payload=payload.serialize(),
                properties=publish_props
            )
            print(f"Placed payload onto topic {topic} Payload Sent: {payload}")
        except Exception as e:
            print(f"An error occurred - {e}")
    else:
        print(f"Missing required header data to successfully transport message - {', '.join(key_diff)}")
        print(message.headers)


# MQTT Functions
def mqtt_on_connect(client: mqtt.Client, userdata: List[str], flags: dict, rc: int, props: Properties = None):
    """
    MQTT Callback for when client receives connection-acknowledgement response from MQTT server.
    :param client: Class instance of connection to server
    :param userdata: User-defined data passed to callbacks, subscription topics
    :param flags: Response flags sent by broker
    :param rc: Connection result, Successful = 0
    :param props: MQTTv5 properties object
    """
    print(f"Connected with result code {rc} -> {mqtt.connack_string(rc)}, properties: {props}")
    # Subscribing in on_connect() allows us to renew subscriptions if disconnected

    if rc == 0 and isinstance(userdata, list):
        if all(isinstance(t, str) for t in userdata):
            client.subscribe([(t.lower(), SUBSCRIBE_OPTIONS) for t in userdata])
            print(f"{client} listening on `{'`, `'.join(t.lower() for t in userdata)}`")
            return
        print("Error in on_connect. Expected userdata to be topics in a list of strings.")


def mqtt_on_publish(client: mqtt.Client, userdata: List[str], mid: int) -> None:
    """
    MQTT Callback for when a publish response is received from the server.
    :param client: Class instance of connection to server.
    :param userdata: User-defined data passed to callbacks
    :param mid:
    """
    print(f"{client} - {userdata} - {mid}")


def mqtt_on_message(client: mqtt.Client, userdata: List[str], msg: mqtt.MQTTMessage):
    """
    MQTT Callback for when a PUBLISH message is received from the broker, forwards to AMQP buffer
    :param client: Class instance of connection to server.
    :param userdata: User-defined data passed to callbacks
    :param msg: Contains payload, topic, qos, retain
    """
    props = {}
    if msg_props := getattr(msg, "properties", None):
        props = msg_props.json()
        props["UserProperty"] = dict(props.get("UserProperty", {}))

    fmt = SerialFormats.from_value(props["UserProperty"].get("encoding", "json"))
    try:
        payload = Message.oc2_loads(msg.payload, fmt)
        print(f"Received: {payload}")

        # copy necessary headers
        headers = {
            "socket": None,  # broker_socket,
            "correlationID": str(payload.request_id),
            "orchestratorID": payload.origin.rsplit("@", 1)[0],
            "encoding": payload.serialization,
            "profile": None,  # profile,
            "transport": "mqtt"
        }

        # Connect and publish to internal buffer
        exchange = "actuator"
        producer = Producer(
            os.environ.get("QUEUE_HOST", "localhost"),
            os.environ.get("QUEUE_PORT", "5672")
        )

        if payload.recipients:
            for recipient in payload.recipients:
                profile, broker_socket = recipient.rsplit("@", 1)
                headers.update(
                    socket=broker_socket,
                    profile=profile,
                )
                producer.publish(
                    headers=headers,
                    message=payload.content,
                    exchange=exchange,
                    routing_key=profile
                )
                print(f"Received: {payload} \nPlaced message onto exchange [{exchange}] queue [{profile}].")
        else:
            producer.publish(
                headers=headers,
                message=payload.content,
                exchange="actuator_all",
                # routing_key="actuator_all"
            )
            print(f"Received: {payload} \nPlaced message onto exchange [actuator_all] queue [actuator_all].")
    except Exception as e:
        print(f"Received: {msg.payload}")
        print(f"MQTT message error: {e}")


def mqtt_on_log(client: mqtt.Client, userdata: List[str], level: int, buf: str) -> None:
    """
    MQTT Callback for when a PUBLISH message is received from the broker, forwards to AMQP buffer
    :param client: Class instance of connection to server.
    :param userdata: User-defined data passed to callbacks
    :param level: MQTT Log Level
    :param buf: the message itself
    """
    lvl = logging.getLevelName(mqtt.LOGGING_LEVEL.get(level, level))
    print(f"{lvl} - {buf}")
