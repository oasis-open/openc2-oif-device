import json, os, re
from flask import Flask, request
from sb_utils import Producer, decode_msg
app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():

    encode = re.search(r'(?<=\+)(.*?)(?=\;)', request.headers['Content-type']).group(1)  # message encoding
    correlationID = request.headers['X-Correlation-ID']  # correlation ID

    data = decode_msg(request.data, encode)  # message being decoded

    host = request.headers['Host'].rsplit('@', 1)
    to = request.headers['From'].rsplit('@', 1)
    profile = host[0]  # profile used
    device = host[1]  # device IP:port
    orchID = to[0]  # orchestrator ID
    orch = to[1]  # orchestrator IP:port

    print('Received command from ' + orch)

    headers = {
        "socket": orch,
        "device": device,
        "correlationID": correlationID,
        "profile": profile,
        "encoding": encode,
        "orchestratorID": orchID,
        "transport": "https"
    }

    producer = Producer()
    producer.publish(message=data, headers=headers, exchange='actuator', routing_key=profile)
    print('Writing to buffer.')

    return json.dumps(dict(
        status=200,
        status_text='received'
    ))


if __name__ == "__main__":
    certPath = '/opt/transport/HTTPS/certs/server.crt'
    keyPath = '/opt/transport/HTTPS/certs/server.key'

    app.run(ssl_context=(certPath, keyPath), host='0.0.0.0', port=5001, debug=True)
