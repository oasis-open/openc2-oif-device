# O.I.F. (OpenC2 Integration Fabric)

## Container/Services ReadMe
### Actuator
- [Base](../device/actuator/Base/ReadMe.md)
- [SLPF](../device/actuator/SLPF/ReadMe.md)

### Transport
- [HTTP](../device/transport/http/ReadMe.md)
- [HTTPS](../device/transport/https/ReadMe.md)
- [MQTT](../device/transport/mqtt/ReadMe.md)

### Logger
- [GUI](../logger/gui/ReadMe.md)
- [Server](../logger/server/ReadMe.md)

#### Default Container/Service
#### Credentials
- No credentials for device

##### Ports
- HTTP - Device: HOST:5000(default)
- HTTPS - Device: HOST:5001(default)
- MQTT - No ports

## Requirements
- Docker v18+
- Docker-Compose v1.20+
- Python 3.6+
- pip 18+

## Getting Started
- Clone/Fork/Download the repo
- Create a local copy on you system, if not downloaded
- Be sure Docker is running

## Configuration
- Run `configure.py` with the desired options prior to starting the Device for the first time
	- Options
    	- `-f FILE` or `--log_file FILE` -- Enables logging to the designated file
    	- `-h` or `--help` -- Shows the help and exits
    	- `-v` or `--verbose` -- Enables verbose output   
    	
    ```bash
    python configure.py [OPTIONS]
    ```

## Running the Compose
### General Info
- Options
	- * `-f FILE` or `--file FILE` -- Specify an alternate compose file (default: docker-compose.yml)
	- `-p NAME` or `--project-name NAME` -- Specify an alternate project name (default: directory name)
	- `-d` or `--detach` -- Detached mode: Run containers in the background, print new container names. Incompatible with --abort-on-container-exit.
- Starting
	- Run the `docker-compose` command for the Device
		
		```bash
		docker-compose ... up [-d]
		```

-  Stopping
	-  If running attached (showing log output, no -d option)
		-  Use 'Ctrl + C' 
	-  If running detached (not showing log output, -d option)
		-  Use the `docker-compose` that was used to start the Device **except** replace `up ...` with `down`
			
			```bash
			docker-compose ... down
			```
- Building Images
	- Run the `docker-compose` that was used to start the Device **except** replace `up ...` with `build`
	- Options
		- SERVICE_NAME - The name of the service (as named in the specified compose file) to rebuild the image, if not specified all services will build if theirs is a context specified
	- Notes
		- Does not need to be run prior to starting, the containers will autobuild if not available
		- Should be run after adding a new Protocol or Serialization
	
	```bash
	docker-compose ... build [SERVICE_NAME]
	```

### Docker Compose Files
#### Central Logging
- __Still Developing__
- Run the `docker-compose` as normal with the additional option of a second '-f/--file'
- Allows for a central location for logging rather than the docker default of per container
- Runs on default port of 8081 for logger web GUI
- Note: If using this option, any additional services should be added to the log yaml

#### Local Central Logging
- Local central logging allows for the logs to be local to the device
- Enabled by using the following command

	```bash
	docker-compose -f device-compose.yaml -f device-compose.log_local.yaml ...
	```

#### Central Logging
- Central logging allows for the logs to be sent to a central location
- Before running this command, edit the `device-compose.log_central.yaml` file such that the `ES_HOST`, `ES_PORT`, and `LOG_PREFIX` of the logger_server service are set properly 
	- ES_HOST - IP/Hostname of the [Elasticsearch](https://www.elastic.co/elasticsearch/) server to send the logs to.  This is the IP/Hostname of the O.I.F. Orchestrator if the central logging is enabled on it.
	- ES_PORT - Port of the Elasticsearch server that is to receive logs, default of 9200
	- LOG_PREFIX - Prefix the logs will show when viewed in the logger gui. Recomended when using multiple devices with the same central logging Elasticsearch.
- Enabled by using the following command

	```bash
	docker-compose -f device-compose.yaml -f device-compose.log_central.yaml ...
	```
 
	
#### Standard Logging
- Use [`docker-compose`](https://docs.docker.com/compose/reference/overview/) to start the device on the system
- Logs are displayed on the terminal with the service name at the start of the line with a randon color for each
- This is the default option if the `-d/--detached` option or central logging is not used

	```bash
	docker-compose -f device-compose.yaml [-p NAME] up [-d]
	```

### Registration
#### Registering a device with the OIF
- Give Device a name and generate a UUID for it.
- Select a transport
    - HTTPS: Enter host and port (Default Port 5001)
    - MQTT: Enter host and port of the broker (Default Port 1883)
	    - See MQTT section in [Transports](./Transport.md) for more info
- Select which serializations in which the device utilizes.
    - Default included device supports JSON, CBOR, and XML.
- Note: include a note about what type of device you are adding.

#### Registering an actuator with the OIF
- Give actuator a name and generate a UUID for it.
- Select a parent device.
    -  Note: device should be registered before the actuator.
- Upload/Copy-Paste schema. Schema for the default included SLPF actuator can be found at [device/actuator/slpf/act_server/schema.json](../device/actuator/slpf/act_server/schema.json).
- This information can also be found under the [SLPF Actuator](../device/actuator/slpf/ReadMe.md) page.
- If you are registering a new actuator for the first time while utilizing the MQTT transport you may need to update the `MQTT_TOPICS` environment variable. Read the MQTT Topics section [here](../transport/mqtt/ReadMe.md)