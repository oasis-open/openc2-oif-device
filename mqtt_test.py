import uuid
import fire
import json
import paho.mqtt.client as mqtt
import time
from base64 import b16encode

'''
Publish an OpenC2 command to MQTT Broker using consumer's TOPIC_C01

Broker address: environment variable CAVBROKER - url:port
Authentication: environment variable CAVUSER - username,password
Command is a JSON string passed via CLI, or defaults to COMMAND_01
'''

# BROKER, BROKER_PORT = os.getenv('CAVBROKER').rsplit(':')
# USERNAME, PASSWORD = os.getenv('CAVUSER').split(',')

# BROKER = '3271a3ddd2eb43caa7c4b195c7d6cabd.s2.eu.hivemq.cloud'
BROKER = 'test.mosquitto.org'
PORT = 1883
# PORT = 8883

USERNAME = 'Cav01'
PASSWORD = 'Tango01Village'
  
# TOPIC_REQUEST = 'oc2/cmd/device/oif'      
TOPIC_REQUEST = 'oc2/cmd/device/th'      
# TOPIC_REQUEST = 'oc2/cmd/device/t01'      
# TOPIC_REQUEST = 'sfractal/command'      
# TOPIC_REQUEST = 'oc2/cmd/ap/er'      
# TOPIC_REQUEST = 'sfractal/command'      
# TOPIC_REQUEST = 'oc2/cmd/device/yuuki_kevin'      

TOPIC_RESPONSE = 'oc2/rsp'
# TOPIC_RESPONSE = 'oc2/rsp/t01'
# TOPIC_P = 'oc2/rsp/p01'                 # This producer's topic
# TOPIC_C01 = 'oc2/cmd/device/c01'        # OpenC2 consumer's topic


COMMAND_01 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': TOPIC_RESPONSE,
        'to': TOPIC_REQUEST,
        'created' : round(time.time() * 1000),
        'actuator_id' : '8144acd3-f5d6-4bda-b1bd-a964f4a19677'
    },
    'body': {
        'openc2': {
            'request': {
                'action': 'investigate',
                'target': {
                    'th': {
                    'hunt': './hunts/find_data_via_stixshifter.hf'
                    }
                }
            }
        }
    }
})

COMMAND_02 = json.dumps({
    'headers': {
        'request_id': str(uuid.uuid4()),
        'from': TOPIC_RESPONSE,
        'to': TOPIC_REQUEST,
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
        'from': TOPIC_RESPONSE,
        'to': TOPIC_REQUEST
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


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    client.subscribe(TOPIC_RESPONSE, 0)
    client.publish(TOPIC_REQUEST, userdata, qos=0, retain=False)
    print(f'Command to {TOPIC_REQUEST}: {userdata}')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    resp = json.loads(msg.payload.decode())
    print(f'Response to {msg.topic}: {resp}')


def main(cmd: str = COMMAND_01, broker: str = BROKER, port: int = int(PORT)):
    client = mqtt.Client(userdata=cmd)
    client.on_connect = on_connect
    client.on_message = on_message

    # client.tls_set()
    # client.username_pw_set(USERNAME.strip(), PASSWORD.strip())
    client.connect(broker, port, 60)
    print(f'Connected to {broker}:{port}')
    client.loop_start()
    time.sleep(1)


if __name__ == '__main__':
    main()