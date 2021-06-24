# OpenC2 Integration Framework FAQ

_Updated 21 April 2020_

* What is OIF?
    * A general-purpose prototyping and testing environment for OpenC2 that includes an Orchestrator (OpenC2 Producer) for generating commands, and a Device (OpenC2 Consumer) that can host one or more Actuators to process and respond to commands.
* What language(s) is OIF implemented in?
    * Orchestrator (Producer)
        * Python (Django RESTful) for the server
        * Javascript (React) for the GUI
    * Device (Consumer)
        * Python
* What external components are required / incorporated?
    * The OIF is built using Docker and as such the only requirement for using OIF is Docker
    * The OIF GUI is built using a standard JavaScript framework and is supported by modern browsers.
    * For the Orchestrator?
        * See ReadMe files of the OIF Orchestrator [services](https://github.com/oasis-open/openc2-oif-orchestrator/tree/master/orchestrator) 
    * For the Device?
        * See ReadMe files of the OIF Device [services](https://github.com/oasis-open/openc2-oif-device/tree/master/device) 
* What OSes are supported for hosting the Docker images?
    * Hosting Docker images follows the same requirements as Docker.  The Docker Registry is a container or set of containers depending on how it is installed/implemented by an individual
    * This is not necessary as the containers are hosted on DockerHub
        * DOCKERHUB URL: TBSL (pending development infrastructure updates)
* What configuration is required once Docker images are installed?
    * Docker configuration is dependent on the system that it has been installed.
    * The configuration of the OIF Orchestrator/Device is handled by the docker-compose file
        * Network IP assignments are irrelevant as  that will be internal to Docker
        * The ONLY IP required is that of the host (system running Docker) and the ports associated with the OIF Orchestrator/Device
    * Example: A Docker host with core services would utilize a different configuration as compared to a development host.
* What transfer protocols are supported Orchestrator-to-Device?
    * Currently the OASIS-standard protocol is [HTTPS](https://docs.oasis-open.org/openc2/open-impl-https/v1.0/open-impl-https-v1.0.html), however CoAP and MQTT have a beta implementations within OIF
* What would be required to add a new transfer protocol?
    * See [transport docs](https://github.com/oasis-open/openc2-oif-orchestrator/blob/master/docs/Transport.md)
* What message encodings are supported Orchestrator-to-Device?
    * Currently the only OASIS-approved serialization is JSON
    * OIF supports schemaless serializations and has reference implementations for [BINN](https://github.com/liteserver/binn/blob/master/spec.md), [BSON](http://bsonspec.org/), [CBOR](https://cbor.io), [MessagePack](https://msgpack.org), S-Expression, XML, [UBJSON](http://ubjson.org/), YAML
* What would be required to add a new message encoding?
    * See [serialization docs](https://github.com/oasis-open/openc2-oif-orchestrator/blob/master/docs/Serializations.md)
* How would a user integrate their own actuator for testing?
    * See Orchestrator/docs/Orchestrator.md#registration
    * Note: The actuator may need to be registered twice under OIF as both a Device and Actuator
* What certificates are being used for HTTPS message transfer?
    * Certificates used are self-signed by default with the ability to use custom certs, see the Orchestrator's [HTTPS transport ReadMe](https://github.com/oasis-open/openc2-oif-orchestrator/tree/master/orchestrator/transport/https)
* What security is applied to MQTT message transfer?
    * Currently there is no security implemented
* How many OIF Devices can an OIF Orchestrator command?
    * Currently there is no defined limit, further usability testing is required to determine this
* How many OIF Orchestrators can an OIF Device respond to?
    * An OIF device responds to the OIF Orchestrator that sent the command
    * At the current implementation of OIF, there is no concept of linking a device to an orchestrator. So, a device can and will respond to ANY orchestrator that it receives a command from.
