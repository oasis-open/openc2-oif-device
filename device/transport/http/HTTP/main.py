import re
import time

from datetime import datetime
from flask import Flask, request, make_response
from multiprocessing import Manager
from sb_utils import decode_msg, encode_msg, default_encode, safe_json, Consumer, Producer

app = Flask(__name__)

manager = Manager()
state = manager.dict()

# state cleaning??
MAX_WAIT = 10


# Error Handling
@app.errorhandler(500)
def internal_error(e):
    print(e)
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
    corr_id = request.headers["X-Request-ID"]  # correlation ID
    # data = decode_msg(request.data, encode)  # message being decoded

    # profile, device_socket = request.headers["Host"].rsplit("@", 1)
    # profile used, device IP:port
    orc_id, orc_socket = request.headers["From"].rsplit("@", 1)
    # orchestrator ID, orchestrator IP:port
    message = request.data
    msg_json = decode_msg(message, encode)

    data = safe_json({
        "headers": dict(request.headers),
        "content": safe_json(message.decode('utf-8'))
    })

    rsp = {
        "status": 200,
        "status_text": "received",
        # command id??
    }

    # Basic verify against language schema??

    # get destination actuator
    actuators = list(msg_json.get('actuator', {}).keys())

    print(f"Received command from {orc_id}@{orc_socket} - {data}")
    if msg_json['action'] == "query" and "command" in msg_json['target']:
        print("QUERY COMMAND")
        cmd_id = msg_json['target']['command']
        prev_cmd = state.get(cmd_id)
        if prev_cmd:
            rsp = {
                "status_text": "previous command found",
                "response": {
                    "command": prev_cmd[0]
                }
            }

    else:
        print("Writing to buffer")
        producer = Producer()
        queue_msg = {
            "message": message,
            "headers": {
                "socket": orc_socket,
                # "device": device_socket,
                "correlationID": corr_id,
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

        print(f"Corr_id: {corr_id}")
        for wait in range(0, MAX_WAIT):
            print(f"Checking for response... {MAX_WAIT} - {wait}")
            rsp_cmd = state.get(corr_id)
            if rsp_cmd:
                rsp = rsp_cmd[0]['body']
                break
            time.sleep(1)

    return make_response(
        # Body
        encode_msg(rsp, encode),
        # Status Code
        200,
        # Headers
        {
            "Content-type": f"application/openc2-rsp+{encode};version=1.0",
            "Status": 200,  # Numeric status code supplied by Actuator's OpenC2-Response
            "X-Request-ID": corr_id,
            "Date": f"{datetime.utcnow():%a, %d %b %Y %H:%M:%S GMT}",  # RFC7231-7.1.1.1 -> Sun, 06 Nov 1994 08:49:37 GMT
            # "From": f"{profile}@{device_socket}",
            # "Host": f"{orc_id}@{orc_socket}",
        }
    )


def process_message(body, message):
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
