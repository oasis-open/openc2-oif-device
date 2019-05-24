# OpenC2 CoAP Transport
Implements CoAP utilizing [CoAPthon3](https://github.com/Tanganelli/CoAPthon3)

## Running Transport
- The CoAP Transport Module is configured to run from a docker container.

## CoAP and OpenC2 Headers

At the time of writing this OpenC2 as well as the OpenC2 CoAP Transport spec have not been finalized. The OpenC2 Headers have been included into the CoAP Request as follows:

```python
request.source = ("localhost", "5683")       # From - IP, Port of CoAP Client sending
request.destination = ("localhost", "5682")  # To - IP, Port of CoAP Server receiving
request.content_type = "application/json"    # Content Type
request.mid = "0x1AB2FE"                     # Request_ID - limited to 16-bits using CoAP
request.timestamp = "Wed, 22 May 2019 16:12:23 UTC", # Created - when message was created by Orchestrator
```

CoAP on the device-side does not need to include any Options because we received enough information to get the OpenC2 Response back to the Orchestrator.

## Port Info

The default port for the CoAP Transport on the Orchestrator side is 5683, the default for registering the demo-device is 5682.