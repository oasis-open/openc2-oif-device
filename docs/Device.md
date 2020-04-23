# O.I.F. (OpenC2 Integration Fabric)

## Container/Services ReadMe
### Actuator
- [ACDCI UC1](../device/actuator/ACDCI_UC1/ReadMe.md)
- [ACDCI UC2](../device/actuator/ACDCI_UC2/ReadMe.md)
- [ACDCI UC3](../device/actuator/ACDCI_UC3/ReadMe.md)
- [ACDCI UC4](../device/actuator/ACDCI_UC4/ReadMe.md)
- [ACDCI UC5](../device/actuator/ACDCI_UC5/ReadMe.md)
- [ACDCI UC6](../device/actuator/ACDCI_UC6/ReadMe.md)
- [ACDCI UC7](../device/actuator/ACDCI_UC7/ReadMe.md)
- [ACDCI UC8](../device/actuator/ACDCI_UC8/ReadMe.md)
- [ACDCI UC9](../device/actuator/ACDCI_UC9/ReadMe.md)
- [Base](../device/actuator/Base/ReadMe.md)
- [EWF](../device/actuator/EWF/ReadMe.md)
- [ISR](../device/actuator/ISR/ReadMe.md)
- [SLPF](../device/actuator/SLPF/ReadMe.md)

### Transport
- [CoAP](../device/transport/coap/README.md)
- [HTTPS](../device/transport/https/README.md)
- [MQTT](../device/transport/mqtt/ReadMe.md)

### Logger
- [GUI](../logger/gui/ReadMe.md)
- [Server](../logger/server/ReadMe.md)

#### Default Container/Service
#### Credentials
- No credentials for device

##### Ports
- CoAP - Device: HOST:5682(default)
- HTTPS - Device: HOST:5001(default)
- MQTT - No ports

## Requirements
- Docker v18+
- Docker-Compose v1.20+
- Python 3.6+
- pip 18+

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
		docker-compose ...... up [-d]
		```

-  Stopping
	-  If running attatched (showing log output, no -d option)
		-  Use 'Ctrl + C' 
	-  If running detatched (not showing log output, -d option)
		-  Use the `docker-compose` that was used to start the Device **except** replace `up ...` with `down`
			
			```bash
			docker-compose ...... down
			```
- Building Images
	- Run the `docker-compose` that was used to start the Device **except** replace `up ...` with `build`
	- Options
		- SERVICE_NAME - The name of the service to rebuild the image, if not specified all will build
	- Notes
		- Does not need to be run prior to starting, the containers will autobuild if not available
		- Should be run after adding a new Protocol or Serialization
	
	```bash
	docker-compose ...... build [SERVICE_NAME]
	```

### Docker Compose Files
### Central Logging
- __Still Developing__
- Run the `docker-compose` as normal with the additional option of a second '-f/--file'
- Allows for a central location for logging rather than the docker default of per container
- Runs on default port of 8081 for logger web GUI

	```bash
	docker-compose -f device-compose.yaml -f device-compose.log.yaml ...
	```
 
- Note: If using this option, any additional containers should be added to the log yaml
 
	
#### Device
- Use [`docker-compose`](https://docs.docker.com/compose/reference/overview/) to start the device on the system

	```bash
	docker-compose -f device-compose.yaml [-p NAME] up [-d]
	```

### Registration
#### Registering a device with the OIF
- Give Device a name and generate a UUID for it.
- Select a transport
    - HTTPS: Enter host and port (Default Port 5001)
    - MQTT: Enter host and port of the broker (Default Port 1883)
- Select which serializations in which the device utilizes.
    - Default included device supports JSON, CBOR, and XML.
- Note: include a note about what type of device you are adding.

#### Registering an actuator with the OIF
- Give actuator a name and generate a UUID for it.
- Select a parent device.
    -  Note: device should be registered before the actuator.
- Upload/Copy-Paste schema. Schema for the default included ISR actuator can be found at [device/actuator/isr/act_server/schema.json](../device/actuator/isr/act_server/schema.json).
- This information can also be found under the [ISR Actuator](../device/actuator/isr/ReadMe.md) page.
- If you are registering a new actuator for the first time while utilizing the MQTT transport you may need to update the `MQTT_TOPICS` environment variable. Read the MQTT Topics section [here](../transport/mqtt/ReadMe.md)