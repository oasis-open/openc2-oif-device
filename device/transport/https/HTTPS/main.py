import json
import re

from flask import Flask, request
from sb_utils import Producer, decode_msg

app = Flask(__name__)


@app.route("/", methods=["POST"])
def result():
    encode = re.search(r"(?<=\+)(.*?)(?=\;)", request.headers["Content-type"]).group(1)  # message encoding
    corrID = request.headers["X-Request-ID"]  # correlation ID
    # data = decode_msg(request.data, encode)  # message being decoded

    profile, device = request.headers["Host"].rsplit("@", 1)
    # profile used, device IP:port
    orchID, orch = request.headers["From"].rsplit("@", 1)
    # orchestrator ID, orchestrator IP:port

    print(f"Received command from {orch}")
    print(f"Data: {{\"\"headers\": {{{request.headers}}}, \"content\": {{{request.data}}}")
    print("Writing to buffer.")
    producer = Producer()
    producer.publish(
        message=request.data,
        headers={
            "socket": orch,
            "device": device,
            "correlationID": corrID,
            "profile": profile,
            "encoding": encode,
            "orchestratorID": orchID,
            "transport": "https"
        },
        exchange="actuator",
        routing_key=profile
    )

    return json.dumps(dict(
        status=200,
        status_text="received"
    ))


if __name__ == "__main__":
    ssl = (
        "/opt/transport/HTTPS/certs/server.crt",  # Cert Path
        "/opt/transport/HTTPS/certs/server.key"   # Key Path
    )

    app.run(ssl_context=ssl, host="0.0.0.0", port=5001, debug=False)
