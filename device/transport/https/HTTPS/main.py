import re

from datetime import datetime
from flask import Flask, request, make_response
from sb_utils import Producer, decode_msg, encode_msg, default_encode, safe_json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def result():
    encode = re.search(r"(?<=\+)(.*?)(?=\;)", request.headers["Content-type"]).group(1)  # message encoding
    corr_id = request.headers["X-Request-ID"]  # correlation ID
    # data = decode_msg(request.data, encode)  # message being decoded

    profile, device_socket = request.headers["Host"].rsplit("@", 1)
    # profile used, device IP:port
    orc_id, orc_socket = request.headers["From"].rsplit("@", 1)
    # orchestrator ID, orchestrator IP:port
    message = request.data

    data = safe_json({
        "headers": dict(request.headers),
        "content": safe_json(message.decode('utf-8'))
    })
    print(f"Received command from {orc_id}@{orc_socket} - {data}")
    print("Writing to buffer.")
    producer = Producer()
    producer.publish(
        message=message,
        headers={
            "socket": orc_socket,
            "device": device_socket,
            "correlationID": corr_id,
            "profile": profile,
            "encoding": encode,
            "orchestratorID": orc_id,
            "transport": "https"
        },
        exchange="actuator",
        routing_key=profile
    )

    return make_response(
        # Body
        encode_msg({
            "status": 200,
            "status_text": "received"
        }, encode),
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


if __name__ == "__main__":
    ssl = (
        "/opt/transport/HTTPS/certs/server.crt",  # Cert Path
        "/opt/transport/HTTPS/certs/server.key"   # Key Path
    )

    app.run(ssl_context=ssl, host="0.0.0.0", port=5001, debug=False)
