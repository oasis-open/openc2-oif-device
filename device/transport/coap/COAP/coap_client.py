from coapthon.client.helperclient import HelperClient
from coapthon.messages.option import Option
from coapthon.utils import generate_random_token
from coapthon import defines

from sb_utils import encode_msg, Consumer
import json

class CoapClient(HelperClient):
 def post(self, path, payload, request, proxy_uri=None, callback=None, timeout=None, **kwargs):
        """
        Perform a POST on a certain path.
        :param path: the path
        :param proxy_uri: Proxy-Uri option of a request
        :param callback: the callback function to invoke upon response
        :param timeout: the timeout of the request
        :return: the response
        """
        request.version = 1
        request.payload = payload
        request.token = generate_random_token(2)

        return self.send_request(request, callback, timeout)


def send_coap(body, message):
    """
    AMQP Callback when we receive a message from internal buffer to be published
    :param body: Contains the message to be sent.
    :param message: Contains data about the message as well as headers
    """
    host, port = message.headers["socket"].split(':')
    path = "transport"

    client = CoapClient(server=(host, port))
    request = client.mk_request(defines.Codes.POST, path)
    response = client.post(
        path, 
        body,
        build_request(request, message.headers)
    )
    if response is not None: print(response.pretty_print())
    client.stop()

def build_request(request, headers):
    """
    Helper method to organized required headers into the CoAP Request.
    :param request: Request being build
    :param headers: Data from AMQP message which contains data to forward OpenC2 Command.
    :param device:  Device specific data from headers sent by O.I.F.
    """
    encoding = "application/" + headers["encoding"]

    source = headers["socket"].split(':')         # location of device-side CoAP server
    request.source = (source[0], int(source[1]))  
    destination = headers["socket"].split(':')    # location of orchestrator-side CoAP server
    request.destination = (destination[0], int(destination[1]))
    request.content_type = defines.Content_types[encoding]   # using application/json, TODO: add define to openc2+json 
    request.mid = headers["correlationID"]                   # 16-bit value - correlationID

    return request

if __name__ == '__main__':
    # Begin consuming messages from internal message queue
    try:
        consumer = Consumer(
            exchange='transport',
            routing_key="coap",
            callbacks=[send_coap]
        )
    except:
        consumer.shutdown()
