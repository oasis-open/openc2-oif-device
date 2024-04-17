import json
import logging
import os
import socket
import time
import traceback

import toml


def build_client_id(custom_name: str = None):
    config_data = toml.load("config.toml")
    
    client_id = config_data["client_id"]
    if custom_name != None:
        client_id = custom_name
        
    curr_millis = current_milli_time()
    client_id = client_id + "-" + socket.gethostname() + "-" + str(curr_millis)
    
    return client_id


def increment(x):
    return x + 1


def decrement(x):
    return x - 1


def load_file(path: str, filename: str):
    data_dict = {}

    try:
        full_path = os.path.join(path,filename)
        with open(full_path, "r") as f:
            data_dict = json.loads(f.read())
          
    except Exception as e:
        logging.error(traceback.format_exc())
        raise Exception("Unable to load schema")  
    
    return data_dict  


def current_milli_time():
    return round(time.time() * 1000)


def is_json(data):
    try:
        json_object = json.loads(data)
    except ValueError as e:
        return False
    return True


def convert_to_dict(data):
    dict_data = {}
    if is_json(data):
        dict_data = json.loads(data)
    return dict_data


def find_file_names_by_extension(ext: str, path: str):
    files_found = []
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if ext in f:
                fp = root + '/' + f
                file_info = {'filename': f, 'fullpath': fp}
                files_found.append(file_info)             
    return files_found