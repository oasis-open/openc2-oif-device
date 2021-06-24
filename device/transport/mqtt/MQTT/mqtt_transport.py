# mqtt_transport.py
import re
import ssl
import uuid
import etcd

from functools import partial
from paho.mqtt import client as mqtt
from sb_utils import Consumer, safe_cast
from time import sleep
from callbacks import mqtt_on_connect, mqtt_on_log, mqtt_on_message, mqtt_on_publish, send_mqtt
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

# Gather topics to subscribe
topics = ['oc2/cmd/all', f'oc2/cmd/device/{dev_uuid}']

sleep(5)
etcd_act_prefix = '/actuator'
try:
    for child in etcd_client.read(etcd_act_prefix, recursive=True, sorted=True).children:
        key = re.sub(fr'^{etcd_act_prefix}/', '', child.key)
        print(f'KEY: {key} -> {child.value}')
        topics.append(f'oc2/cmd/ap/{key}')
except etcd.EtcdKeyNotFound:
    print('No actuators found')

client = mqtt.Client(
    client_id=dev_id,
    # Add prefix if specified
    userdata=['/'.join(filter(None, [*Config.MQTT_PREFIX.split('/'), *t.split('/')])) for t in topics],
    protocol=mqtt.MQTTv5
)

# set auth
if Config.USERNAME:
    client.username_pw_set(
        username=Config.USERNAME,
        password=Config.PASSWORD
    )

# check that certs exist
if Config.TLS_ENABLED:
    client.tls_insecure_set(safe_cast(Config.TLS_SELF_SIGNED, bool, False))
    client.tls_set(
        ca_certs=Config.CAFILE,
        certfile=Config.CLIENT_CERT,
        keyfile=Config.CLIENT_KEY,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

# TODO: add optional etcd watcher via ENV vars
client.on_log = mqtt_on_log
client.on_connect = mqtt_on_connect
client.on_publish = mqtt_on_publish
client.on_message = mqtt_on_message

client.connect(
    host=Config.MQTT_HOST,
    port=Config.MQTT_PORT,
    keepalive=300,
    clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY
)

client.loop_start()

# Begin consuming messages from internal message queue
consumer = None
try:
    consumer = Consumer(
        exchange='transport',
        routing_key="mqtt",
        callbacks=[partial(send_mqtt, Config)]
    )
except Exception as err:
    print(f"Consumer Error: {err}")
    consumer.shutdown()
