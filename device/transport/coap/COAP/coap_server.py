import os

from coapthon import defines
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

from sb_utils import decode_msg, encode_msg, Producer


class TransportResource(Resource):
    def __init__(self, name="TransportResource", coap_server=None):
        super(TransportResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

    def render_POST_advanced(self, request, response):
        # retrieve Content_type stored as dict of types:values (ex. "application/json": 50)
        encoding = [k for k, v in defines.Content_types.items() if v == request.content_type]
        encoding = "json" if len(encoding) != 1 else encoding[0].split("/")[1]

        # read custom options added for O.I.F. and retrieve them based on their number
        # opts = {o.name: o.value for o in request.options}

        profile_opt = list(filter(lambda o: o.number == 8, request.options))
        route = profile_opt[0].value if len(profile_opt) == 1 else None

        socket_opt = list(filter(lambda o: o.number == 3, request.options))
        socket = socket_opt[0].value if len(socket_opt) == 1 else None

        print(f"{encoding}-{type(encoding)} -- {route}-{type(route)}")
        if encoding and route:
            print(f"Sending msg to {route}")
            # Create headers for the orchestrator from the request
            headers = dict(
                correlationID=request.mid,
                socket=socket,
                encoding=encoding,
                transport="coap"
                # orchestratorID="orchid1234",    # orchestratorID is currently an unused field, this is a placeholder
            )

            # Send request to actuator
            try:
                producer = Producer(os.environ.get("QUEUE_HOST", "localhost"), os.environ.get("QUEUE_PORT", "5672"))
                producer.publish(
                    message=decode_msg(request.payload, encoding),
                    headers=headers,
                    exchange="actuator",
                    routing_key=route
                )
                response.payload = encode_msg({
                    "status": 200,
                    "status_text": "received"
                }, encoding)
                response.code = defines.Codes.CONTENT.number
            except Exception as e:
                print(e)
                response.payload = e
                return self, response

        else:
            print(f"Not enough info: {encoding} - {route}")
            response.payload = encode_msg({
                    "status": 400,
                    "status_text": "Not enough data to send message to actuator"
                }, encoding)

            response.code = defines.Codes.BAD_REQUEST.number

        return self, response


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource("transport/", TransportResource())


if __name__ == "__main__":
    server = CoAPServer("0.0.0.0", 5683)
    try:
        print("Server listening on 0.0.0.0:5683")
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")
