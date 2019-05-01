# mqtt_transport.py

import paho.mqtt.client as mqtt
import os
import ssl
from sb_utils import Consumer, safe_cast
from callbacks import Callbacks

# Begin consuming messages from internal message queue
try:
    consumer = Consumer(
        exchange='transport',
        routing_key="mqtt",
        callbacks=[Callbacks.send_mqtt]
    )
except:
    consumer.shutdown()

# begin listening to a single MQTT socket
client = mqtt.Client()
print("Initializing client...")

# check that certs exist
if os.environ.get('MQTT_TLS_ENABLED', False):
    client.tls_set(ca_certs=os.environ.get('MQTT_CAFILE', None),
                    certfile=os.environ.get('MQTT_CLIENT_CERT', None),
                    keyfile=os.environ.get('MQTT_CLIENT_KEY', None))
    client.username_pw_set(os.environ.get('MQTT_DEFAULT_USERNAME', 'guest'), os.environ.get('MQTT_DEFAULT_PASS', 'guest'))
    client.tls_insecure_set(os.environ.get('MQTT_TLS_SELF_SIGNED', 0))

client.connect(os.environ.get('MQTT_HOST', 'queue'), safe_cast(os.environ.get('MQTT_PORT', 1883), int, 1883))

topics = os.environ.get('MQTT_TOPICS', None)
topics = topics.split(', ')

client.user_data_set(topics)
client.on_connect = Callbacks.on_connect
client.on_message = Callbacks.on_message
client.loop_start()

    