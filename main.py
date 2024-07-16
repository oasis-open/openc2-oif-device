

import toml
import uvicorn
import logging, logging.config, yaml

from transports import mqtt
from utils import utils

config_data = toml.load("config.toml")
client_id = utils.build_client_id()

def devicelogger():
    return logging.getLogger('file')

def get_logconsole():
    return logging.getLogger('console')

if __name__ == "__main__":

    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    loader = yaml.safe_load(open('logging.conf'))
    logging.config.dictConfig(loader)
    logfile    = devicelogger()
    logconsole = get_logconsole()
    
    logfile.debug("Debug FILE -- App Started")
    logconsole.debug("Debug CONSOLE -- App Started")    

    config_data = toml.load("config.toml")
    is_http_enabled = config_data["HTTP"]["is_enabled"]
    is_mqtt_enabled = config_data["MQTT"]["is_enabled"]

    if is_mqtt_enabled:
        mqtt.set_user_pw()  # Needed for AWS and MQHIV Brokers
        mqtt.connect_to_broker()
        mqtt.subscribe_to_topics()

        if not is_http_enabled:
            mqtt.client.loop_forever()
        else:
            mqtt.client.loop_start()

    else:
        print("MQTT is disabled, to adjust this see the config.toml file")

    if is_http_enabled:
        host = config_data["HTTP"]["host"]
        port = config_data["HTTP"]["port"]
        log_Level = config_data["HTTP"]["log_Level"]

        uvicorn.run("api:app", host=host, port=port, log_level=log_Level, app_dir="./transports")
    else:
        print("HTTP is disabled, to adjust this see the config.toml file")        