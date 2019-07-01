# callbacks.py

import json
import os
import paho.mqtt.publish as publish
import re

from sb_utils import Consumer, Producer, encode_msg, decode_msg, safe_cast

# maintains a list of active devices we can receive responses from
ACTIVE_CONNECTIONS = []


class Callbacks(object):
    required_header_keys = {"encoding", "orchestratorID", "socket"}

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        MQTT Callback for when client receives connection-acknowledgement response from MQTT server.
        :param client: Class instance of connection to server
        :param userdata: User-defined data passed to callbacks
        :param flags: Response flags sent by broker
        :param rc: Connection result, Successful = 0
        """
        print(f"Connected with result code {rc}")
        # Subscribing in on_connect() allows us to renew subscriptions if disconnected

        if isinstance(userdata, list):
            for topic in userdata:
                if not isinstance(topic, str):
                    print("Error in on_connect. Expected topic to be type a list of strings.")
                client.subscribe(topic.lower(), qos=1)
                print(f"Listening on {topic.lower()}")

    @staticmethod
    def on_message(client, userdata, msg):
        """
        MQTT Callback for when a PUBLISH message is received from the broker, forwards to AMQP buffer
        :param client: Class instance of connection to server.
        :param userdata: User-defined data passed to callbacks
        :param msg: Contains payload, topic, qos, retain
        """
        payload = json.loads(msg.payload)
        payload_header = payload.get("header", {})

        encoding = re.search(r"(?<=\+)(.*?)(?=;)", payload_header.get("content_type", "")).group(1)
        profile, broker_socket = payload_header.get("to", "").rsplit("@", 1)
        orc_id = payload_header.get("from", "").rsplit("@", 1)[0]
        corr_id = payload_header.get("correlationID", "")

        # copy necessary headers
        header = {
            "socket": broker_socket,
            "correlationID": corr_id,
            "orchestratorID": orc_id,
            "encoding": encoding,
            "profile": profile,
            "transport": "mqtt"
        }

        # Connect and publish to internal buffer
        exchange = "actuator"
        producer = Producer(
            os.environ.get("QUEUE_HOST", "localhost"),
            os.environ.get("QUEUE_PORT", "5672")
        )

        producer.publish(
            headers=header,
            message=payload.get("body", ""),
            exchange=exchange,
            routing_key=profile
        )
        
        print(f"Received: {payload} \nPlaced message onto exchange [{exchange}] queue [{profile}].")

    @ staticmethod
    def send_mqtt(body, message):
        """
        AMQP Callback when we receive a message from internal buffer to be published to MQTT Broker
        :param body: Contains the message to be sent.
        :param message: Contains data about the message as well as headers
        """
        # check for certs if TLS is enabled
        if os.environ.get("MQTT_TLS_ENABLED", False) and os.listdir("/opt/transport/MQTT/certs"):
            tls = dict(
                ca_certs=os.environ.get("MQTT_CAFILE", None),
                certfile=os.environ.get("MQTT_CLIENT_CERT", None),
                keyfile=os.environ.get("MQTT_CLIENT_KEY", None)
            )
        else:
            tls = None

        # build message for MQTT
        encoding = message.headers.get("encoding", "json")
        broker_socket = message.headers.get("socket", "localhost:1883")
        content_type = f"application/openc2-cmd+{encoding};version=1.0"
        source = f"{message.headers.get('profile', '')}@{broker_socket}"
        dest = f"{message.headers.get('orchestratorID', '')}@{broker_socket}"
        corr_id = message.headers.get("correlationID", "")

        payload = {
            "header": {
                "to": dest,
                "from": source,
                "correlationID": corr_id,
                "content_type": content_type
            },
            "body": body
        }

        # Transport is running on device side, send response to orchestrator
        key_diff = Callbacks.required_header_keys.difference({*message.headers.keys()})
        if len(key_diff) == 0:
            ip, port = broker_socket.split(":")[0:2]
            topic = message.headers.get("orchestratorID") + "/response"
            try:
                publish.single(
                    topic,
                    payload=json.dumps(payload),
                    qos=1,
                    hostname=ip,
                    port=safe_cast(port, int, 1883),
                    will={
                        "topic": topic,
                        "payload": json.dumps(payload),
                        "qos": 1
                    },
                    tls=tls,
                )
                print(f"Sent: {payload}")
            except Exception as e:
                print(f"An error occurred -  {e}")
                pass
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
