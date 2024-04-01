import signal
import ssl
import sys
import traceback
import uuid
import json
import paho.mqtt.client as mqtt
import time
from base64 import b16encode
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

import toml

'''
Publish an OpenC2 command to MQTT Broker
'''

client_id = "mqtt_tester_" + str(uuid.uuid4())
to = "test_receiver"

config_data = toml.load("config.toml")
default_broker = config_data["MQTT"]["broker"]
default_port = config_data["MQTT"]["port"]
default_protocol = config_data["MQTT"]["protocol"]

default_cmd_topics = config_data["MQTT"]["listen_topics"]
default_rsp_topics = config_data["MQTT"]["resp_topics"]        

default_username = config_data["MQTT"]['username']  
default_password = config_data["MQTT"]['password']

# TODO: Add / pull client id from file to retain longer than just session time
device_topic = "oc2/cmd/device/" + client_id
default_cmd_topics.append(device_topic)


# BROKER, BROKER_PORT = os.getenv('CAVBROKER').rsplit(':')
# USERNAME, PASSWORD = os.getenv('CAVUSER').split(',')

# BROKER = '3271a3ddd2eb43caa7c4b195c7d6cabd.s2.eu.hivemq.cloud'
# BROKER = 'test.mosquitto.org'
# PORT = 1883
# PORT = 8883

# USERNAME = 'Cav01'
# PASSWORD = 'Tango01Village'
  
# TOPIC_REQUEST = 'oc2/cmd/device/oif'      
# TOPIC_REQUEST = 'oc2/cmd/ap/hunt'      
# TOPIC_REQUEST = 'oc2/cmd/device/t01'      
# TOPIC_REQUEST = 'sfractal/command'      
# TOPIC_REQUEST = 'oc2/cmd/ap/er'      
# TOPIC_REQUEST = 'sfractal/command'      
# TOPIC_REQUEST = 'oc2/cmd/device/yuuki_kevin'      
TOPIC_REQUEST = 'oc2/cmd/all'      

TOPIC_RESPONSE = 'oc2/rsp'
# TOPIC_RESPONSE = 'oc2/rsp/t01'
# TOPIC_P = 'oc2/rsp/p01'                 # This producer's topic
# TOPIC_C01 = 'oc2/cmd/device/c01'        # OpenC2 consumer's topic

COMMAND_00 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000),
        'actuator_id' : '8144acd3-f5d6-4bda-b1bd-a964f4a19677'
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/huntflow/query_web_stixdata.hf'
                    }
                }
            }
        }
    }
})


COMMAND_01 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000),
        'actuator_id' : '8144acd3-f5d6-4bda-b1bd-a964f4a19677'
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/huntflow/find_data_via_stixshifter.hf'
                    }
                }
            }
        }
    }
})

COMMAND_02 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000),
        'actuator_id' : '8144acd3-f5d6-4bda-b1bd-a964f4a19677'        
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'scan',
                'target': {
                    'device': 'test'
                },
                'actuator' : 'er'
            }
        }
    }
})

COMMAND_03 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'query',
                'target': {
                     'sbom': {  'content':  'cyclone' }
                },
                'actuator' : 'sbom'
            }
        }
    }
})

COMMAND_04 = json.dumps(
    {
        "action": "set", 
        "target": {
            "blinky:led": "off"
        }, 
        "args": {
            "response_requested": "complete"
        }
    }
)

COMMAND_05 = json.dumps(
    {
        "action": "set",
        "target": {"x-sfractal-blinky:led": "rainbow"},
        "args": {"response_requested": "complete"}
    }

)

COMMAND_06 = json.dumps(
    {
        "action": "set",
        "target": {"blinky:led": "rainbow"},
        "args": {"response_requested": "complete"}
    }

)

COMMAND_07 = json.dumps(
    {
        "action": "set",
        "target": {"blinky:led": "off"},
        "args": {"response_requested": "complete"}
    }

)


# catch ctrl-c
def signal_handler(signum, frame):
    graceful_shutdown()
    

def graceful_shutdown():
    print()
    # the will_set is not sent on graceful shutdown by design
    # we need to wait until the message has been sent, else it will not appear in the broker
    global client
    publish_result = client.publish(TOPIC_RESPONSE, payload = "offline", qos = 0, retain = True)
    publish_result.wait_for_publish() 
    
    client.disconnect()
    client.loop_stop()
    sys.exit()


def on_connect5(client, userdata, flags, rc, properties):
    print("mqtt: New mqtt instance connected")
    # client.subscribe("$SYS/#")
    client.connected_flag=True    


def on_connect(client, userdata, flags, rc):
    print("mqtt: New mqtt instance connected")
    # client.subscribe("$SYS/#")
    client.connected_flag=True    
    

def on_log(client, userdata, level, buf):
    print("mqtt: ", buf)     


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    try:
        msg_str = str(message.payload.decode("utf-8"))
        print("MQTT Message Received *")
        print("\t Message \t=" ,msg_str)
        print("\t Topic \t\t=",message.topic)
        print("\t QOS \t\t=",message.qos)
        print("\t Retain flag \t=",message.retain)  
        
    except Exception as e:
        print(traceback.format_exc())
        status = 500
        work_result = "Error processing mqtt message response: " + traceback.format_exc()        


def publish(topic = None, msg = "test"):

    if topic is None:
        topic = default_rsp_topics[0]

    print("mqtt: Publishing ->")
    print("\t Topic \t\t=" ,topic)        
    print("\t Message \t=" ,msg)        
    b_msg = msg.encode('utf-8').strip()     

    openc2_properties = Properties(PacketTypes.PUBLISH)
    if "v3" in default_protocol:
        openc2_properties = None  
    else:
        openc2_properties.PayloadFormatIndicator = 1
        openc2_properties.ContentType = 'application/openc2'
        openc2_properties.UserProperty = [('msgType', 'cmd'), ('encoding', 'json')] 

    qos = 0
    retain = False

    global client
    return client.publish(topic, b_msg, qos, retain, openc2_properties)  


def set_user_pw(user: str = None, pw: str = None):

    if user is None:
        user = default_username

    if pw is None:
        pw = default_password

    global client
    client.username_pw_set(user, pw)
    client.tls_set(certfile=None,
                    keyfile=None,
                    cert_reqs=ssl.CERT_REQUIRED)  


def connect_to_broker(broker: str = None, port: str = None):

    if broker is None:
        broker = default_broker

    if port is None:
        port = default_port      

    try:
        global client
        client.connect(broker, port) 
    except Exception:
        print("mqtt: Unable to connect to MQTT Broker")
        print(traceback.format_exc())  


def subscribe_to_topics(topics: list = [TOPIC_RESPONSE]):
    for topic in topics:
        print("mqtt: Subscribing to Topic: ", topic)
        global client
        client.subscribe(topic)       


def shutdown():
    print("Shutting down MQTT Instance: ", client_id)
    global client
    client.disconnect()
    client.loop_stop()


def main():
    test = ""


if __name__ == '__main__':
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    print("MQTT Instance Started")
    print("\t Client ID \t\t= ", client_id)
    print("\t Default Broker \t= ", default_broker)
    print("\t Default Port \t\t= ", default_port)
    print("\t Default Protocol \t= ", default_protocol)
    print("\t Default CMD Topics \t= ", default_cmd_topics)
    print("\t Default RSP Topics \t= ", default_rsp_topics)
    print() 

    if default_protocol == "MQTTv5":
        client.on_connect = on_connect5
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, None, userdata=True, protocol=mqtt.MQTTv5, transport="tcp") 
    else:
        client.on_connect = on_connect
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, None, userdata=True, protocol=mqtt.MQTTv311, transport="tcp")     


    client.on_message = on_message
    client.on_log = on_log

    is_mqtt_enabled = config_data["MQTT"]["is_enabled"]

    if is_mqtt_enabled:
        set_user_pw()  # Needed for AWS and MQHIV Brokers
        connect_to_broker()
        subscribe_to_topics()
        signal.signal(signal.SIGINT, signal_handler)
        publish(TOPIC_REQUEST, COMMAND_00)
        client.loop_forever()
    else:
        print("MQTT is not enabled")    
    
    main()