# OpenC2 MQTT Transport
Implements MQTT utilizing [Paho MQTT](https://www.eclipse.org/paho/clients/python/docs/).


[![pipeline status](https://gitlab.labs.g2-inc.net/ScreamingBunny/Orchestrator/Core/badges/develop/pipeline.svg)](https://gitlab.labs.g2-inc.net/ScreamingBunny/Orchestrator/Core/commits/develop)

## Running Transport
- The MQTT Transport Module is configured to run from a docker container.

1. Install Docker

2. Build/Pull container

    - Build:
    ```
    docker login gitlab.labs.g2-inc.net:4567
    docker build -f Dockerfile -t gitlab.labs.g2-inc.net:4567/screamingbunny/transport/MQTT .
    ```

    - Pull:   
    ```
    docker login gitlab.labs.g2-inc.net:4567
    docker pull gitlab.labs.g2-inc.net:4567/screamingbunny/transport/MQTT
    ```

3. Start the container

    - Use dev-compose.yaml, this will pull latest image from gitlab and start the service.
    ```
    docker-compose -f dev-compose.yaml up
    ```

    - To ensure docker-compose stopped properly, use:
    ```
    docker-compose -f dev-compose.yaml down
    ```
# Setup

## MQTT Topics

The MQTT transport is subscribed to a [topic](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices) that is related to the actuator that the OpenC2 message should be routed to. The current convention is topic=actuatorProfileName (eg. openc2_isr_actuator_profile).

The environment variable `MQTT_TOPICS` is a string of comma-separated topics (lists are unsupported) that can be appended to when new actuators are added. The `MQTT_TOPICS` variable is preset to contain the topics relating to the included default actuator(s).

## Broker Location

If running the OIF as the Orchestrator and Device on a single machine, the RabbitMQ MQTT Broker will build as a part of the device stack. Otherwise, the RabbitMQ MQTT Broker host should be specified as the environment variable `MQTT_HOST` which should contain the ip or hostname of the desired MQTT Broker.

## Ports

Default port for [RabbitMQ MQTT](https://www.rabbitmq.com/mqtt.html) Broker is `1883` or `8883` if TLS is activated for RabbitMQ MQTT. Can be modified through the `MQTT_PORT` environment variable (default 1883)

Read/Writes to an internal RabbitMQ AMQP Broker at default port `5672` on the orchestrator side and `5673` on the device side. All ports can be edited under the Docker Compose file under the queue port options.

## Adding certificates for TLS

To enable TLS set the environment variable `MQTT_TLS_ENABLE` to `1`

To indicate the use of self-signed certificates (not for production use) set the environment variable `MQTT_TLS_SELF_SIGNED` to `1`. For self-signed certificates, RabbitMQ recommends [tls-gen](https://github.com/michaelklishin/tls-gen).

The cert files needed to activate TLS are specified as environment variables: `MQTT_CAFILE`, `MQTT_CLIENT_CERT`, `MQTT_CLIENT_KEY`

If your broker is configured to require a username and password, use environment variables: `MQTT_DEFAULT_USERNAME`, `MQTT_DEFAULT_PASS`

To add the certificates uncomment the line in the Dockerfile `ADD certs /opt/transport/MQTT/certs` where `ADD <source> <dest>`


