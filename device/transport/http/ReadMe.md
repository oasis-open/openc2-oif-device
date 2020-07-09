# OASIS TC Open: oif-device-transport-http
## OpenC2 HTTP Transport

### About this Image
- This is the OpenC2 HTTP transfer container for use with the O.I.F.

### How to use this image
#### Transport Setup
- The HTTP Transport Module is configured to run from a docker container as a part of the OIF-Orchestrator docker stack. Use the [configure.py](../../../configure.py) script to build the images needed to run the entirety of this Transport as a part of the Orchestrator.

#### Starting Container
 - To start the container

    - Use dev-compose.yaml, this will pull latest image from gitlab and start the service.
    ```
    docker-compose -f dev-compose.yaml up
    ```
