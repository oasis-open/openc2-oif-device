import traceback
from benedict import benedict
from fastapi import FastAPI, Request, Response
import toml
from oc2.message_manager import build_response_msg, process_oc2_msg, validate_msg_required_properties, validate_schema
from main import client_id

from utils.const import DESC, TITLE, VERSION
from utils.utils import current_milli_time, load_file


app = FastAPI(
    title=TITLE,
    description=DESC,
    version=VERSION
)


@app.get("/")
async def hello_world():
    return {"Hello FastAPI World!"}


@app.post("/.well-known/openc2_command")
async def openc2_command(command: Request, response: Response):
    print("HTTP Message Received *")

    oc2_response = {}  
    try:
        
        msg = {
            "headers" : {},
            "body" : {}
        }

        # Get Headers
        header_data = {}
        for key, value in command.headers.items():
            header_data[key] = value  
        msg['headers'] = header_data

        # Get Body
        msg['body'] = await command.json()
        
        # Load Schema
        config_data = toml.load("config.toml")
        path = config_data["schema_path"]
        filename = config_data["schema_file"]
        schema_dict = load_file(path, filename)

        # Validate Schema
        invalid_schema = validate_schema(schema_dict)
        if invalid_schema:
            raise Exception(invalid_schema)

        # Validate Message against Schema
        msg_benedict = benedict(msg)
        invalid_msg = validate_msg_required_properties(msg_benedict)
        if invalid_msg:
            raise Exception(invalid_msg)        

        # Do work... 
        status_int = 200
        status_text = "Success"
        oc2_response = "No work performed"    
        if invalid_schema == None and invalid_msg == None:          
            oc2_response = process_oc2_msg(msg_benedict)

    except Exception as e:
        print(traceback.format_exc())
        status_int = 500
        status_text = "Error"
        oc2_response = "Error processing http command: " + traceback.format_exc()

    resp_body = build_response_msg(status_int, status_text, oc2_response)        
                
    # Response Headers
    if msg_benedict.headers.request_id is not None:
        response.headers["request_id"] = msg_benedict.headers.request_id
    response.headers["created"] = str(current_milli_time())
    response.headers["from"] = client_id

    return resp_body



