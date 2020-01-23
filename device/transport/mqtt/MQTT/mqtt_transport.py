# mqtt_transport.py

import os
import paho.mqtt.client as mqtt
import time

from sb_utils import Consumer, safe_cast
from callbacks import Callbacks

# Begin consuming messages from internal message queue
try:
    consumer = Consumer(
        exchange='transport',
        routing_key="mqtt",
        callbacks=[Callbacks.send_mqtt]
    )
except Exception as err:
    print(f"Consumer Error: {err}")
    consumer.shutdown()

# begin listening to a single MQTT socket
client = mqtt.Client()
print("Initializing client...")

# check that certs exist
if os.environ.get('MQTT_TLS_ENABLED', False):
    client.tls_set(
        ca_certs=os.environ.get('MQTT_CAFILE', None),
        certfile=os.environ.get('MQTT_CLIENT_CERT', None),
        keyfile=os.environ.get('MQTT_CLIENT_KEY', None)
    )
    client.username_pw_set(
        os.environ.get('MQTT_DEFAULT_USERNAME', 'guest'),
        os.environ.get('MQTT_DEFAULT_PASS', 'guest')
    )
    client.tls_insecure_set(os.environ.get('MQTT_TLS_SELF_SIGNED', 0))

client.connect(
    os.environ.get('MQTT_HOST', 'queue'),
    safe_cast(os.environ.get('MQTT_PORT', 1883), int, 1883)
)

topics = []
if "TRANSPORT_TOPICS" in os.environ:
    time.sleep(2)
    transports = [t.lower().strip() for t in os.environ.get("TRANSPORT_TOPICS", "").split(",")]
    topics.extend([t.lower().strip() for t in consumer.get_queues() if t not in transports])

if "MQTT_TOPICS" in os.environ:
    topics.extend([t.lower().strip() for t in os.environ.get("MQTT_TOPICS", "").split(",") if t not in topics])

client.user_data_set(topics)
client.on_connect = Callbacks.on_connect
client.on_message = Callbacks.on_message
client.loop_start()
