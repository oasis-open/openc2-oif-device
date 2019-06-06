import json
import urllib3

from datetime import datetime
from sb_utils import Consumer, encode_msg


def process_message(body, message):
    """
    Callback when we receive a message from internal buffer to publish to waiting flask.
    :param body: Contains the message to be sent.
    :param message: Contains data about the message as well as headers
    """
    http = urllib3.PoolManager(cert_reqs="CERT_NONE")

    body = body if isinstance(body, dict) else json.loads(body)
    rcv_headers = message.headers

    orc_socket = rcv_headers["socket"]  # orch IP:port
    orc_id = rcv_headers["orchestratorID"]  # orchestrator ID
    corr_id = rcv_headers["correlationID"]  # correlation ID

    device_socket = rcv_headers["device"]  # device IP:port
    encoding = rcv_headers["encoding"]  # message encoding
    profile = rcv_headers["profile"]  # profile used

    if orc_socket and encoding:
        print(f"Sending response to {orc_id}@{orc_socket}")

        try:
            r = http.request(
                method="POST",
                url=f"https://{orc_socket}",
                body=encode_msg(body, encoding),  # command being encoded
                headers={
                    "Content-type": f"application/openc2-rsp+{encoding};version=1.0",
                    "Status": body.get("status", 200),  # Numeric status code supplied by Actuator's OpenC2-Response
                    "X-Request-ID": corr_id,
                    "Date": f"{datetime.utcnow():%a, %d %b %Y %H:%M:%S GMT}",  # RFC7231-7.1.1.1 -> Sun, 06 Nov 1994 08:49:37 GMT
                    "From": f"{profile}@{device_socket}",
                    "Host": f"{orc_id}@{orc_socket}",
                }
            )
            print(f"Data: {{\"\"headers\": {{{r.request.headers}}}, \"content\": {{{r.request.data}}}")
            print(f"Response from request: {r.status}")
        except Exception as err:
            err = str(getattr(err, "message", err))
            print(f"HTTPS error: {err}")
    else:
        print("Destination/Encoding of response not specified")


if __name__ == "__main__":
    print("Connecting to RabbitMQ...")
    try:
        consumer = Consumer(
            exchange="transport",
            routing_key="https",
            callbacks=[process_message]
        )

    except Exception as err:
        print(f"Consumer Error: {err}")
        consumer.shutdown()
