# OpenC2 HTTPS Transport

[![pipeline status](https://gitlab.labs.g2-inc.net/ScreamingBunny/Orchestrator/Core/badges/develop/pipeline.svg)](https://gitlab.labs.g2-inc.net/ScreamingBunny/Orchestrator/Core/commits/develop)

## Transport Setup
- The HTTPS Transport Module is configured to run from a docker container.

1. Install Docker

2. Build/Pull container

    - Build:
    ```
    docker login gitlab.labs.g2-inc.net:4567
    docker build -f Dockerfile -t gitlab.labs.g2-inc.net:4567/screamingbunny/transport/HTTPS .
    ```

    - Pull:   
    ```
    docker login gitlab.labs.g2-inc.net:4567
    docker pull gitlab.labs.g2-inc.net:4567/screamingbunny/transport/HTTPS
    ```

## Configuration

### Adding Own Certs

- The user has the option of adding personal certs instead of self signed generated certs on startup in development mode.
 
1. Generate certs to be used.
 
2. Put certs into the certs folder.
    
    - Certs Folder:
    ```
    /HTTPS/certs
    ```
    - Rename the certs for the flask app:
    ```
    server.crt
    server.key
    ```
    
3. Edit the transport file to use certs.

    - Edit line in https_transport.py
    ```
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    to
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=/opt/transport/HTTPS/certs/CERTNAME)
    ```
    
4. Edit Dockerfile

    - Remove self-signed certificate generation.
    ```
    RUN openssl genrsa -des3 -passout pass:x -out /opt/transport/HTTPS/certs/server.pass.key 2048 && \
    openssl rsa -passin pass:x -in /opt/transport/HTTPS/certs/server.pass.key -out /opt/transport/HTTPS/certs/server.key && \
    rm /opt/transport/HTTPS/certs/server.pass.key && \
    openssl req -new -key /opt/transport/HTTPS/certs/server.key -out /opt/transport/HTTPS/certs/server.csr \
        -subj "/C=US/O=flask/OU=Screaming Bunny" && \
    openssl x509 -req -days 365 -in /opt/transport/HTTPS/certs/server.csr -signkey /opt/transport/HTTPS/certs/server.key -out /opt/transport/HTTPS/certs/server.crt
    ```

## Starting Container
 - To start the container

    - Use dev-compose.yaml, this will pull latest image from gitlab and start the service.
    ```
    docker-compose -f dev-compose.yaml up
    ```
