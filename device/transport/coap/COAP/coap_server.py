from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.response import Response
from coapthon import defines

from sb_utils import Producer, decode_msg

import os, json

class TransportResource(Resource):
    def __init__(self, name="TransportResource", coap_server=None):
        super(TransportResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

    def render_POST_advanced(self, request, response):

        # retrieve Content_type stored as dict of types:values (ex. "application/json": 50)
        for content_type, val in defines.Content_types.items():
            if request.content_type == val:
                encoding = content_type.split('/')[1]

        # read custom options added for O.I.F. and retrieve them based on their value (order shifts when options are added)
        for opt in request.options:
            try:
                # value is a socket
                if len(opt.value.split(':')) == 2:
                    socket = opt.value
                # value is an actuator profile name
                elif len(opt.value.split('_')) > 1:
                    route = opt.value
            except:
                continue

        if encoding and route: 
            # Create headers for the orchestrator from the request
            headers = dict(
                correlationID=request.mid,
                socket=socket,
                encoding=encoding,
                transport='coap'
                #orchestratorID='orchid1234',    # orchestratorID is currently an unused field, this is a placeholder
            )
            
            # Send request to actuator
            try:
                producer = Producer(os.environ.get('QUEUE_HOST', 'localhost'), os.environ.get('QUEUE_PORT', '5672'))
                producer.publish(
                    message=decode_msg(request.payload, encoding), 
                    headers=headers, 
                    exchange="actuator", 
                    routing_key=route
                )
                response.payload = "Message successfully received."
                response.code = defines.Codes.CONTENT.number
            except Exception as e:
                print(e)
                response.payload = e
                return self, response

        else:
            response.payload = "Not enough data to send message to actuator"
            response.code = defines.Codes.BAD_REQUEST.number

        return self, response
    
class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('transport/', TransportResource())


if __name__ == '__main__':

    server = CoAPServer("0.0.0.0", 5682)
    try:
        print("Server listening on 0.0.0.0:5682")
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")


