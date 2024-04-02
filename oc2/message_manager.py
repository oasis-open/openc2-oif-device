import json
import logging
import traceback
from benedict import benedict
from typing import Union

import toml

from hunts.py.find_data_via_huntflow_j2 import hunt_via_file_j2
from hunts.py.find_data_via_huntflow import hunt_via_file
from hunts.py.find_data_via_variables import hunt_via_variables
from utils.utils import current_milli_time, find_file_names_by_extension
from jsonschema import Validator, validate

HEADERS_REQUEST_ID_PATH = "headers.request_id"
ACTION_PATH = "body.openc2.request.action"
TARGET_PATH = "body.openc2.request.target"
QUERY_FEATURES_PATH = "body.openc2.request.target.features"
TH_HUNT_PATH = "body.openc2.request.target.th.hunt"
TH_HUNTBOOKS_PATH = "body.openc2.request.target.th.huntflows.path"
TH_DATASOURCES_PATH = "body.openc2.request.target.th.datasources"
TH_HUNTARGS_STRING_ARGS_PATH = "body.openc2.request.args.th.huntargs.string_args"


def build_response_msg(status_int: int, status_text: str = None, results: any = None):
    response_msg = {
        "openc2": {
            "response": {
                "status": status_int,
                "status_text": status_text,
                "results": results
            }
        }
    }   

    return response_msg


def build_response_msg_bytes(request_id: str, from_str: str, status_int: int, results: any = None):
    response_msg = {
        "headers": {
            "request_id": request_id,
            "created": current_milli_time(),
            "from": from_str
        },
        "body": {
            "openc2": {
                "response": {
                    "status": status_int,
                    "results": results
                }
            }
        }
    }   

    return json.dumps(response_msg)

def validate_schema(schema: dict):
    try:
        Validator.check_schema(schema)
    except Exception as e:
        logging.error(traceback.format_exc())
        return "Invalid schema"
    return None 

def validate_msg_required_properties(msg: Union[dict, benedict]):

    if isinstance(msg, dict):
        msg_benedict = benedict(msg)

    if not msg_benedict:
        return "unable to process message"
    
    if "headers" not in msg_benedict:
        return "message missing 'headers'"
    
    if HEADERS_REQUEST_ID_PATH not in msg_benedict:
        return "message missing 'headers / request_id'" 
    
    if "headers.created" not in msg_benedict:
        return "message missing 'headers / created'"    

    if "headers.from" not in msg_benedict:
        return "message missing 'headers / from'"        
    
    if "body" not in msg_benedict:
        return "message missing 'body'"      

    if "body.openc2" not in msg_benedict:
        return "message missing 'body / openc2'"       

    if "body.openc2.request" not in msg_benedict:
        return "message missing 'body / openc2 / request'"               
    
    if ACTION_PATH not in msg_benedict:
        return "message missing 'body / openc2 / request / action'"       
    
    if TARGET_PATH not in msg_benedict:
        return "message missing 'body / openc2 / request / target'"           

    return None

def validate_msg_against_schema(message_dict: dict, schema: dict):
    invalid_msg = None

    try:
        validate(instance=message_dict, schema=schema)
    except Exception as e:
        err = traceback.format_exc()
        logging(err)
        invalid_msg = "Invalid Message"     

    return invalid_msg

def validate_oc2_msg(message_dict: dict, schema: dict):
    invalid_msg = validate_msg_against_schema(message_dict, schema)
    invalid_msg = validate_msg_required_properties(message_dict)
    return invalid_msg

def process_oc2_msg(msg_benedict: benedict):

    # TODO: Move Kestrel specific logic under a kestrel message manager

    work_result = ""
    config_data = toml.load("config.toml")
    is_kestrel_enabled = config_data["KESTREL"]["is_enabled"]

    if msg_benedict[ACTION_PATH]  == "query":                      

        if is_kestrel_enabled:
            if QUERY_FEATURES_PATH in msg_benedict:
                work_result = {"version": 1,
                        "pairs": "[investigate:hunt]",
                        "rate_limit": 1,
                        "profiles": "th"
                        }

            elif TH_HUNTBOOKS_PATH in msg_benedict: 
                huntbooks_path = msg_benedict[TH_HUNTBOOKS_PATH]
                work_result = find_file_names_by_extension(".jhf", huntbooks_path)

            elif TH_DATASOURCES_PATH in msg_benedict:
                work_result = config_data["KESTREL"]["datasources"]

    elif msg_benedict[ACTION_PATH]  == "investigate":  

        if is_kestrel_enabled:
            if TH_HUNT_PATH in msg_benedict:
                hunt_path = msg_benedict[TH_HUNT_PATH] 
                hunt_args = []
                if ".jhf" in hunt_path:
                    if TH_HUNTARGS_STRING_ARGS_PATH in msg_benedict:
                        hunt_args = msg_benedict[TH_HUNTARGS_STRING_ARGS_PATH]
                    work_result = hunt_via_file_j2(hunt_path, hunt_args)

            #elif TH_HUNT_PATH in msg_benedict:
            #    hunt_path = msg_benedict[TH_HUNT_PATH] 
            #    work_result = hunt_via_file(hunt_path)

    # TODO: Add other interactions here ...

    if not work_result:
        who = config_data["name"]
        action_type = msg_benedict[ACTION_PATH]
        work_result = f"{action_type} action completed by {who}"

    return work_result