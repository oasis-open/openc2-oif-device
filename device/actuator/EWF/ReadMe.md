# OpenC2 EWF Actuator

#### Notes:
- N/A


## Running the Actuator
- Server is configured to run a docker container

1. Install docker

2. Update submodules
    
    ```bash
    git submodule update --remote
    ```

3. Build/pull container
    - Build
    
    ```bash
    docker login gitlab.labs.g2-inc.net:4567
    docker build -f Dockerfile -t gitlab.labs.g2-inc.net:4567/screamingbunny/actuator/ewf .
    ```
    
    - Pull
    
    ```bash
    docker login gitlab.labs.g2-inc.net:4567
    docker pull gitlab.labs.g2-inc.net:4567/screamingbunny/actuator/ewf
    ```

4. Start the container
    - Note: There should be a RabbitMQ and transport container/instance for the core to connect to

- Development
    - Note: To reload the scripts, restart the container
    
     ```bash
    docker run \
	--hostname core \
	--name core \
    -e QUEUE_HOST=queue \
    -e QUEUE_PORT=5672 \
    -e QUEUE_USER=guest \
    -e QUEUE_PASSWORD=guest \
    -e QUEUE_EXCHANGE=device \
    -e QUEUE_ACTUATOR_KEY=actuator \
    -v $(PWD)/act_server:/opt/actuator/act_server \
	--link queue \
	--rm \
    gitlab.labs.g2-inc.net:4567/screamingbunny/actuator/ewf
	```
    
- Production
    
    ```bash
     docker run \
	--hostname core \
	--name core \
    -e QUEUE_HOST=queue \
    -e QUEUE_PORT=5672 \
    -e QUEUE_USER=guest \
    -e QUEUE_PASSWORD=guest \
    -e QUEUE_EXCHANGE=device \
    -e QUEUE_ACTUATOR_KEY=actuator \
	--link queue \
	--rm \
    gitlab.labs.g2-inc.net:4567/screamingbunny/actuator/ewf
	```
