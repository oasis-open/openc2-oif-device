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
from utils import utils

import toml

'''
Publish an OpenC2 command to MQTT Broker
'''

client_id = utils.build_client_id("mqtt_tester")
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
# device_topic = "oc2/cmd/device/" + client_id
# default_cmd_topics.append(device_topic)

# TODO: Move Test Commands to another file
COMMAND_Q0 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'query',
                'target': {
                    'features': ["versions", "profiles"]
                }
            }
        }
    }
})

COMMAND_Q1 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'query',
                'target': {
                    'th': {
                        'huntflows': 'hunts/huntflow'
                    }
                }
            }
        }
    }
})

COMMAND_Q2 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'query',
                'target': {
                    'th': {
                        'datasources': 'hunts/huntflow'
                    }
                }
            }
        }
    }
})

COMMAND_CASP_00 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/jinja/oc2-hunt-1.jhf'
                    }
                }
            }
        }
    }
})

COMMAND_CASP_01 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/jinja/oc2-hunt-2.jhf'
                    }
                },
                'args': {
                    'th': {
                    'huntargs': {
                        "string_args": ["filename_1:disablefw.json", "filename_2:hosts.json"]
                        }
                    }
                }
            }
        }
    }
})

COMMAND_CASP_02 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/jinja/oc2-hunt-3.jhf'
                    }
                },
                'args': {
                    'th': {
                    'huntargs': {
                        "string_args": ["filename_1:disablefw.json", "filename_2:hosts.json"]
                        }
                    }
                }
            }
        }
    }
})

COMMAND_CASP_03 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': client_id,
        'to': to,
        'created' : round(time.time() * 1000)
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/jinja/oc2-hunt-4.jhf'
                    }
                },
                'args': {
                    'th': {
                    'huntargs': {
                        "string_args": ["filename_1:siblings.json", "filename_2:hosts.json"]
                        }
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
        'created' : round(time.time() * 1000)
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
        'created' : round(time.time() * 1000)       
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
    
def graceful_shutdown(client: mqtt.Client):
    print()
    publish_result = client.publish(default_rsp_topics[0], payload = "offline", qos = 0, retain = True)
    publish_result.wait_for_publish() 
    
    client.disconnect()
    client.loop_stop()
    sys.exit()
    
def shutdown(client: mqtt.Client):
    print("Shutting down MQTT Instance: ", client_id)
    client.disconnect()
    client.loop_stop()    
 

def on_connect5(client: mqtt.Client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.connected_flag=True   
    client.is_connected
    client.subscribe(default_rsp_topics)
    

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.connected_flag=True   
    client.is_connected    
    client.subscribe(default_rsp_topics)
    

def on_log(client, userdata, level, buf):
    print("mqtt: ", buf)     


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


def publish(client: mqtt.Client, topic = None, msg = "test"):

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

    return client.publish(topic, b_msg, qos, retain, openc2_properties)  


def set_user_pw(client: mqtt.Client, user: str = None, pw: str = None):

    if user is None:
        user = default_username

    if pw is None:
        pw = default_password

    if user and pw:
        client.username_pw_set(user, pw)
        client.tls_set(certfile=None,
                        keyfile=None,
                        cert_reqs=ssl.CERT_REQUIRED) 


def connect_to_broker(client: mqtt.Client, broker: str = None, port: str = None):

    if broker is None:
        broker = default_broker

    if port is None:
        port = default_port      

    try:
        client.connect(broker, port) 
    except Exception:
        print("mqtt: Unable to connect to MQTT Broker")
        print(traceback.format_exc())  


def subscribe_to_topics(client: mqtt.Client, topics: list = default_rsp_topics):
    for topic in topics:
        print("mqtt: Subscribing to Topic: ", topic)
        client.subscribe(topic)       


def main():
    test = ""


if __name__ == '__main__':
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    print("MQTT Instance Started")
    print("\t Client ID \t\t= ", client_id)
    print("\t Broker \t= ", default_broker)
    print("\t Port \t\t= ", default_port)
    print("\t Protocol \t= ", default_protocol)
    print("\t CMD Topics \t= ", default_cmd_topics)
    print("\t RSP Topics \t= ", default_rsp_topics)
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
        set_user_pw(client)  # Needed for AWS and MQHIV Brokers
        client.connect(default_broker, default_port)
        client.subscribe(default_rsp_topics[0])
        publish(client, default_cmd_topics[0], COMMAND_CASP_00)
        client.loop_forever()
    else:
        print("MQTT is not enabled")    
    
    main()