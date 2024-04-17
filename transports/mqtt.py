import ssl
import traceback
import paho.mqtt.client as mqtt

from benedict import benedict
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
import toml
from oc2.message_manager import HEADERS_REQUEST_ID_PATH, build_response_msg_bytes, process_oc2_msg, validate_msg_required_properties, validate_schema

from utils.utils import convert_to_dict, find_file_names_by_extension, load_file
from main import client_id, devicelogger


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
        openc2_properties.UserProperty = [('msgType', 'rsp'), ('encoding', 'json')] 

    qos = 0
    retain = False
    
    devicelogger().debug("mqtt -- publishing msg ***")
    devicelogger().debug("mqtt -- topic: %s", topic)
    devicelogger().debug("mqtt -- rsp msg: %s", msg)    

    return client.publish(topic, b_msg, qos, retain, openc2_properties)


def on_message(client, userdata, message):
    try:
        # time.sleep(4) # Waiting 2 secs (remove) once producer has redis
        
        msg_str = str(message.payload.decode("utf-8"))
        # print("MQTT Message Received *")
        # print("\t Message \t=" ,msg_str)
        # print("\t Topic \t\t=",message.topic)
        # print("\t QOS \t\t=",message.qos)
        # print("\t Retain flag \t=",message.retain)  
        
        devicelogger().debug("mqtt -- msg received ***")
        devicelogger().debug("mqtt -- topic: %s", message.topic)
        devicelogger().debug("mqtt -- msg: %s", msg_str) 

        message_dict = convert_to_dict(msg_str)
        msg_benedict = benedict(message_dict)

        # Load Schema
        config_data = toml.load("config.toml")
        path = config_data["schema_path"]
        filename = config_data["schema_file"]
        schema_dict = load_file(path, filename)
        
        # Validate
        invalid_schema = validate_schema(schema_dict)
        if invalid_schema:
            raise Exception(invalid_schema)

        invalid_msg = validate_msg_required_properties(msg_benedict)
        if invalid_msg:
            raise Exception(invalid_msg)

        # Do work... 
        status = 200
        work_result = "No work performed"    
        if invalid_schema == None and invalid_msg == None:          
            work_result = process_oc2_msg(msg_benedict)

    except Exception as e:
        print(traceback.format_exc())
        status = 500
        work_result = "Error processing mqtt message: " + traceback.format_exc()

    # Build Response
    response_msg = build_response_msg_bytes(msg_benedict[HEADERS_REQUEST_ID_PATH],
                                    client_id,
                                    status,
                                    work_result)   

    publish(default_rsp_topics[0], response_msg)


def set_user_pw(user: str = None, pw: str = None):

    if user is None:
        user = default_username

    if pw is None:
        pw = default_password

    if user and pw:
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
        client.connect(broker, port) 
    except Exception:
        print("mqtt: Unable to connect to MQTT Broker")
        print(traceback.format_exc())  


def subscribe_to_topics(topics: list = None):

    if topics is None:
        topics = []
        topics.extend(default_cmd_topics)

    for topic in topics:
        print("mqtt: Subscribing to Topic: ", topic)
        client.subscribe(topic)       


def shutdown():
    print("Shutting down MQTT Instance: ", client_id)
    client.disconnect()
    client.loop_stop()


config_data = toml.load("config.toml")
default_broker = config_data["MQTT"]["broker"]
default_port = config_data["MQTT"]["port"]
default_protocol = config_data["MQTT"]["protocol"]

default_cmd_topics = config_data["MQTT"]["listen_topics"]
default_rsp_topics = config_data["MQTT"]["resp_topics"]        

default_username = config_data["MQTT"]['username']  
default_password = config_data["MQTT"]['password'] 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if default_protocol == "MQTTv5":
    client.on_connect = on_connect5
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, None, userdata=True, protocol=mqtt.MQTTv5, transport="tcp") 
else:
    client.on_connect = on_connect
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, None, userdata=True, protocol=mqtt.MQTTv311, transport="tcp") 

client.on_message = on_message
client.on_log = on_log

print("MQTT Instance Started")
print("\t Client ID \t\t= ", client_id)
print("\t Default Broker \t= ", default_broker)
print("\t Default Port \t\t= ", default_port)
print("\t Default Protocol \t= ", default_protocol)
print("\t Default CMD Topics \t= ", default_cmd_topics)
print("\t Default RSP Topics \t= ", default_rsp_topics)
print()         

hb_path = config_data["KESTREL"]["huntbook_paths"][0]
print("Kestrel Info:")
print("\t Datasources \t\t= ", config_data["KESTREL"]["datasources"])
print("\t Huntbook Paths \t= ", config_data["KESTREL"]["huntbook_paths"])
print("\t Huntbooks Available \t= ",  find_file_names_by_extension("hf", hb_path))
print()  