import re
import time
import uuid
import kombu

from datetime import datetime
from multiprocessing import Manager
from typing import Union
from flask import Flask, request, make_response
from sb_utils import Consumer, Message, MessageType, Producer, SerialFormats, decode_msg, safe_json

app = Flask(__name__)

manager = Manager()
state = manager.dict()

# state cleaning??
MAX_WAIT = 30


# Error Handling
@app.errorhandler(500)
def internal_error(e):
    print(f"HTTP Server Error: {e}")
    return make_response(
        # Body
        {
            'status': 500,
            'status_text': 'Internal Error - The Consumer transport encountered an unexpected condition that prevented it from performing the Command.'
        },
        # Status Code
        500
    )


@app.route("/", methods=["POST"])
def result():
    encode = re.search(r"(?<=\+)(.*?)(?=\;)", request.headers["Content-type"]).group(1)  # message encoding
    fmt = SerialFormats.from_value(encode)
    try:
        cmd = Message.oc2_loads(request.data, fmt)
    except Exception as e:
        print(f"Message load Error: {e}")
        cmd = Message(
            recipients=request.headers.get("Host", ""),
            origin=request.headers.get("From", ""),
            created=datetime.strptime(request.headers.get("Date"), "%a, %d %b %Y %H:%M:%S GMT"),
            msg_type=MessageType.Request,
            request_id=uuid.UUID(request.headers.get("X-Request-ID", "")),  # Header correlation ID
            content_type=fmt,
            content=decode_msg(request.data, fmt)
        )

    # profile used, device IP:port
    profile, device_socket = request.headers["Host"].rsplit("@", 2)
    # orchestrator ID, orchestrator IP:port
    orc_id, orc_socket = cmd.origin.rsplit("@", 2)
    data = safe_json({
        "headers": dict(request.headers),
        "content": cmd.content
    })

    rsp = Message(
        recipients=cmd.origin,
        # origin=request.headers.get("From", ""),  # TODO: how??
        msg_type=MessageType.Response,
        request_id=cmd.request_id,
        content_type=cmd.content_type,
        content={
            "status": 200,
            "status_text": "received",
            # command id??
        }
    )
    # TODO: Basic verify against language schema??
    # get destination actuator
    actuators = list(cmd.content.get('actuator', {}).keys())

    print(f"Received command from {cmd.origin} - {data}")
    if cmd.content['action'] == "query" and "command" in cmd.content['target']:
        print("QUERY COMMAND")
        if prev_cmd := state.get(cmd.content['target']['command'], None):
            rsp.content = {
                "status_text": "previous command found",
                "response": {
                    "command": prev_cmd[0]
                }
            }

    else:
        print("Writing to buffer")
        producer = Producer()
        queue_msg = {
            "message": cmd.content,
            "headers": {
                "socket": orc_socket,
                # "device": device_socket,
                "correlationID": cmd.request_id,
                # "profile": profile,
                "encoding": encode,
                "orchestratorID": orc_id,
                "transport": "http"
            }
        }
        if len(actuators) == 0:
            print('No NSIDs specified, Send to all')
            try:
                producer.publish(
                    **queue_msg,
                    exchange="actuator_all",
                    exchange_type="fanout",
                    routing_key="actuator_all"
                )
            except Exception as e:
                print(f'Publish Error: {e}')
        else:
            print(f'NSIDs specified - {actuators}')
            for act in actuators:
                producer.publish(
                    **queue_msg,
                    exchange="actuator",
                    routing_key=act
                )

        print(f"Corr_id: {cmd.request_id}")
        for wait in range(0, MAX_WAIT):
            print(f"Checking for response... {MAX_WAIT} - {wait}")
            if rsp_cmd := state.get(cmd.request_id, None):
                rsp.content = rsp_cmd[0]['body']
                break
            time.sleep(1)

    return make_response(
        # Body
        rsp.serialize(),
        # Status Code
        200,
        # Headers
        {
            "Content-type": f"application/openc2-rsp+{encode};version=1.0",
            "Status": 200,  # Numeric status code supplied by Actuator's OpenC2-Response
            "X-Request-ID": rsp.request_id,
            "Date": f"{rsp.created:%a, %d %b %Y %H:%M:%S GMT}",  # RFC7231-7.1.1.1 -> Sun, 06 Nov 1994 08:49:37 GMT
            # "From": f"{profile}@{device_socket}",
            # "Host": f"{orc_id}@{orc_socket}",
        }
    )


def process_message(body: Union[dict, str], message: kombu.Message) -> None:
    """
    Callback when we receive a message from internal buffer to publish to waiting flask.
    :param body: Contains the message to be sent.
    :param message: Contains data about the message as well as headers
    """
    body = body if isinstance(body, dict) else safe_json(body)
    rcv_headers = message.headers

    # Device Info
    profile = rcv_headers["profile"]  # profile used

    rcv_time = f"{datetime.utcnow():%a, %d %b %Y %H:%M:%S GMT}"
    print(f"Received command from {profile}@{rcv_time} - {body}")
    corr_id = rcv_headers["correlationID"]
    rsp = dict(
        received=rcv_time,
        headers=rcv_headers,
        body=body
    )
    if corr_id in state:
        state[corr_id].append(rsp)
    else:
        state[corr_id] = [rsp]


if __name__ == "__main__":
    print("Connecting to RabbitMQ...")
    try:
        consumer = Consumer(
            exchange="transport",
            routing_key="http",
            callbacks=[process_message],
            debug=True
        )
    except Exception as err:
        print(f"Consumer Error: {err}")
        consumer.shutdown()

    app.run(host="0.0.0.0", port=5001, debug=False)
