# callbacks.py

from urllib.parse import urlparse
from sb_utils import Consumer, Producer, encode_msg, decode_msg
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import os
import json
import socket
import re

class Callbacks(object):

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        MQTT Callback for when client receives connection-acknowledgement response from MQTT server.
        :param client: Class instance of connection to server
        :param userdata: User-defined data passed to callbacks
        :param flags: Response flags sent by broker
        :param rc: Connection result, Successful = 0
        """
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() allows us to renew subscriptions if disconnected

        if type(userdata) is list:
            for topic in userdata:
                if type(topic) is not str:
                    print('Error in on_connect. Expected topic to be type a list of strings.')
                client.subscribe(topic.lower(), qos=1)
                print('Listening on', topic.lower())

    @staticmethod
    def on_message(client, userdata, msg):
        """
        MQTT Callback for when a PUBLISH message is received from the broker, forwards to AMQP buffer
        :param client: Class instance of connection to server.
        :param userdata: User-defined data passed to callbacks
        :param msg: Contains payload, topic, qos, retain
        """
        payload = json.loads(msg.payload)
        encoding = re.search(r'(?<=\+)(.*?)(?=\;)', payload["header"].get('content_type', '')).group(1)  # message encoding
        route, socket = payload["header"].get('to', '').rsplit('@', 1)
        orchestratorID = payload["header"].get('from', '').rsplit('@', 1)[0]
        correlationID = payload["header"].get('correlationID', '')

        header = {
            "socket": socket,
            "correlationID": correlationID,
            "encoding": encoding,
            "orchestratorID": orchestratorID,
            "profile": route,
            "transport": "mqtt"
        }

        exchange = 'actuator'

        # Connect and publish to internal buffer
        producer = Producer(os.environ.get('QUEUE_HOST', 'localhost'),
                            os.environ.get('QUEUE_PORT', '5672'))

        producer.publish(
            headers=header,
            message=payload.get('body', ''),
            exchange=exchange,
            routing_key=route
        )    
        
        print(f'Received: {payload} \nPlaced message onto exchange [{exchange}] queue [{route}].')

    @ staticmethod
    def send_mqtt(body, message):
        """
        AMQP Callback when we receive a message from internal buffer to be published to MQTT Broker
        :param body: Contains the message to be sent.
        :param message: Contains data about the message as well as headers
        """
        
        payload = {}

        # check for certs if TLS is enabled
        if os.environ.get('MQTT_TLS_ENABLED', False) and os.listdir('/opt/transport/MQTT/certs'):
            tls = dict(
                ca_certs=os.environ.get('MQTT_CAFILE', None),
                certfile=os.environ.get('MQTT_CLIENT_CERT', None),
                keyfile=os.environ.get('MQTT_CLIENT_KEY', None)
            )
        else:
            tls = None

        # build message for MQTT
        encoding = message.headers.get('encoding', 'json')
        socket = message.headers.get('socket', 'localhost:1883')
        content_type = "application/openc2-cmd+" + encoding + ";version=1.0"
        source = message.headers.get('profile', '') + '@' + socket
        dest = message.headers.get('orchestratorID', '') + '@' + socket
        correlationID = message.headers.get('correlationID', '')

        payload['header'] = {
            "to": dest,
            "from": source,
            "correlationID": correlationID,
            "content_type" : content_type
        }

        payload['body'] = body

        # Transport is running on device side, send response to orchestrator
        if all(keys in message.headers for keys in ['socket', 'encoding', 'orchestratorID']):

            ip, port = socket.split(':')[0:2]
            topic = message.headers.get('orchestratorID') + '/response'
            try:
                publish.single(
                    topic,
                    payload=json.dumps(payload),
                    hostname=ip,
                    port=int(port),
                    tls=tls,
                    qos=1
                )
                print(f'Sent: {payload}')
            except Exception as e:
                print(f'An error occured. {e}')
                pass
        else:
            print('Missing some/all required header data to successfully transport message.')
            print(message.headers)

# maintains a list of active devices we can receive responses from
ACTIVE_CONNECTIONS = []

def send_error_response(e, header):
    """
    If error occurs before leaving the transport on the orchestrator side, then send back a message
    response to the internal buffer indicating so.
    :param e: Exception thrown 
    :param header: Include headers which would have been sent for Orchestrator to read.
    """
    producer = Producer(
        os.environ.get('QUEUE_HOST', 'localhost'),
        os.environ.get('QUEUE_PORT', '5672')
    )
    producer.publish(
        headers=header,
        message=json.dumps(str(e)),
        exchange='orchestrator',
        routing_key='response'
    )    
    print(f'Error Response Sent.')