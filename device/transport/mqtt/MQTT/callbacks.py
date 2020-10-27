# callbacks.py
import json
import os
import uuid

from paho.mqtt import client as mqtt, publish
from sb_utils import Message, MessageType, Producer, SerialFormats, toStr
from typing import Any


class Callbacks:
    required_header_keys = {"encoding", "orchestratorID", "socket"}

    @staticmethod
    def on_connect(client: mqtt.Client, userdata: Any, flags: dict, rc: int):
        """
        MQTT Callback for when client receives connection-acknowledgement response from MQTT server.
        :param client: Class instance of connection to server
        :param userdata: User-defined data passed to callbacks
        :param flags: Response flags sent by broker
        :param rc: Connection result, Successful = 0
        """
        print(f"Connected with result code {rc} -> {mqtt.connack_string(rc)}")
        # Subscribing in on_connect() allows us to renew subscriptions if disconnected

        if rc == 0 and isinstance(userdata, list):
            if not all(isinstance(t, str) for t in userdata):
                print("Error in on_connect. Expected topic to be type a list of strings.")
                return
            print(f"{client} listening on `{'`, `'.join(t.lower() for t in userdata)}`")
            for topic in userdata:
                client.subscribe(topic.lower(), qos=1)

    @staticmethod
    def on_message(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage):
        """
        MQTT Callback for when a PUBLISH message is received from the broker, forwards to AMQP buffer
        :param client: Class instance of connection to server.
        :param userdata: User-defined data passed to callbacks
        :param message: Contains payload, topic, qos, retain
        """
        payload = Message.unpack(message.payload)
        print(f'Received: {payload}')

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

    @ staticmethod
    def send_mqtt(body, message, client: mqtt.Client):
        """
        AMQP Callback when we receive a message from internal buffer to be published to MQTT Broker
        :param body: Contains the message to be sent.
        :param message: Contains data about the message as well as headers
        :param client: MQTT connection
        """
        # Get message pieces
        broker_socket = message.headers.get("socket", "localhost:1883")

        # build message for MQTT
        payload = Message(
            recipients=f"{message.headers.get('orchestratorID', '')}@{broker_socket}",
            origin=f"{message.headers.get('profile', '')}@{broker_socket}",
            # created: datetime = None,
            msg_type=MessageType.Response,
            request_id=uuid.UUID(message.headers.get("correlationID", "")),
            serialization=SerialFormats.from_value(message.headers.get("encoding", "json")),
            content=body if isinstance(body, dict) else json.loads(body)
        ).pack()

        # Transport is running on device side, send response to orchestrator
        key_diff = Callbacks.required_header_keys.difference({*message.headers.keys()})
        if len(key_diff) == 0:
            params = ['_client_id', '_host', '_port', '_username', '_password', '_ssl_context']
            params = {k[1:]: getattr(client, k) for k in params}

            # TODO: validate response topic
            topic = 'oc2/rsp'
            try:
                publish.single(
                    topic,
                    client_id=f"{toStr(params['client_id'])}-pub",
                    payload=payload,
                    qos=1,
                    retain=False,
                    hostname=params['host'],
                    port=params['port'],
                    keepalive=60,
                    will=None,
                    # Authentication
                    auth=dict(
                        username=params['username'],
                        password=params['password'] or None
                    ) if params['username'] else None,
                    tls=params['ssl_context'] or None
                )
                print(f"Placed payload onto topic {topic} Payload Sent: {payload}")
            except Exception as e:
                print(f"An error occurred - {e}")
        else:
            print(f"Missing required header data to successfully transport message - {', '.join(key_diff)}")
            print(message.headers)


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
