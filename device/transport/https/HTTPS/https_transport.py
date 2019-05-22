import json, os, urllib3
from sb_utils import Consumer, encode_msg


def process_message(body, message):
    """
    Callback when we receive a message from internal buffer to publish to waiting flask.
    :param body: Contains the message to be sent.
    :param message: Contains data about the message as well as headers
    """

    params = message.headers
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')

    des = params['socket']  # orch IP:port
    device = params['device']  # device IP:port
    encode = params['encoding']  # message encoding
    prof = params['profile']  # profile used
    orchID = params['orchestratorID']  # orchestrator ID
    correlation = params['correlationID']  # correlation ID

    print('Sending command to ' + des)

    if des and encode:
        headers = {
            "Host": orchID+"@"+des,
            "From": prof+"@"+device,
            "Content-type": "application/openc2-cmd+"+encode+";version=1.0",
            "X-Correlation-ID": correlation,
        }

        try:
            r = http.request('POST', 'https://' + des, body=body, headers=headers)
            print(r.status)
        except Exception as err:
            print(err)

    else:
        print("Destination or encoding of message not specified.")

print("Connecting to RabbitMQ...")
try:
    consumer = Consumer(
        exchange="transport",
        routing_key="https",
        callbacks=[process_message])

except Exception as error:
    print(error)
    consumer.shutdown()
