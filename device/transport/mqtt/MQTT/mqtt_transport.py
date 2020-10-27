# mqtt_transport.py
import re
import uuid
import etcd

from functools import partial
from paho.mqtt import client as mqtt
from sb_utils import Consumer, safe_cast
from time import sleep
from callbacks import Callbacks
from config import Config

# Connect to Etcd
etcd_client = etcd.Client(
    host=Config.ETCD_HOST,
    port=Config.ETCD_PORT
)

# Generate/Get 23 character Device ID from ...
try:
    dev_uuid = uuid.UUID(etcd_client.read('/device/id').value)
except etcd.EtcdKeyNotFound:
    dev_uuid = uuid.uuid4()
    etcd_client.write('/device/id', str(dev_uuid))
dev_id = f'device_{str(dev_uuid).replace("-", "")[:15]}'


# begin listening to a single MQTT socket
print(f"Initializing Device: {dev_uuid}...")
client = mqtt.Client(
    client_id=dev_id,
    # clean_session=None
)

# check that certs exist
if Config.TLS_ENABLED:
    client.tls_insecure_set(safe_cast(Config.TLS_SELF_SIGNED, bool, False))
    client.tls_set(
        ca_certs=Config.CAFILE,
        certfile=Config.CLIENT_CERT,
        keyfile=Config.CLIENT_KEY
    )

if Config.USERNAME:
    client.username_pw_set(
        username=Config.USERNAME,
        password=Config.PASSWORD
    )

client.connect(
    host=Config.MQTT_HOST,
    port=Config.MQTT_PORT,
    # keepalive=60,
    # clean_start=MQTT_CLEAN_START_FIRST_ONLY
)

# Gather topics to subscribe
topics = [
    'oc2/cmd/all',
    f'oc2/cmd/device/{dev_uuid}'
]

sleep(5)
etcd_act_prefix = '/actuator'
try:
    for child in etcd_client.read(etcd_act_prefix, recursive=True, sorted=True).children:
        key = re.sub(fr'^{etcd_act_prefix}/', '', child.key)
        print(f'KEY: {key} -> {child.value}')
        topics.append(f'oc2/cmd/ap/{key}')
except etcd.EtcdKeyNotFound:
    print('No actuators found')

# Add prefix if specified
topics = ['/'.join(filter(None, [*Config.MQTT_PREFIX.split('/'), *t.split('/')])) for t in topics]

# TODO: add optional etcd watcher via ENV vars

client.user_data_set(topics)
client.on_connect = Callbacks.on_connect
client.on_message = Callbacks.on_message
client.loop_start()

# Begin consuming messages from internal message queue
consumer = None
try:
    consumer = Consumer(
        exchange='transport',
        routing_key="mqtt",
        callbacks=[
            partial(Callbacks.send_mqtt, client=client)
        ]
    )
except Exception as err:
    print(f"Consumer Error: {err}")
    consumer.shutdown()
