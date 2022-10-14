# OpenC2 Actuator

#### Notes:
- N/A

## Developing an Actuator
- Actuators are configured to run as Docker containers by default

1. Copy the `Base` actuator folder and rename it for the actuator being created
	- Note: the container will be tagged the same as the folder name; folder - `SLPF`, image - `.../actuator:slpf`
	- Note: All following steps are assumed to be from within this new folder
	- If a `config.json` file exists in the `act_server` folder, delete the file

2. Replace the `schema.json` file with the schema of the actuator being created
	- Note: The actuator can currently only validate the commands/responses with a JSON Schema

3. Create a python file in the `act_server/actions` folder for an action that is supported by the actuator with the following contents, replacing `ACTION` with the action being created.
	- Note: If the file exists, skip to step 3
	- Note: The `ACTION` in quotes should be lowercase and appear as it does within the OpenC2 Language Spec
	- Note: The default function is necessary and does not need to return the specified value as specified, but an OpenC2 formatted python dictionary is required

	```python
	"""
	ACTION Target functions
	"""
    from sb_utils import FrozenDict
    from sb_utils.actuator import Dispatch, exceptions
	
	ACTION = Dispatch("ACTION")
	
	@ACTION.register
	def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()
	```
	
4. Within the newly created action file, create a function for a target supported by the action of the actuator and either add the register decorator to the function or register the function after declaration
	- Note: The function does not need to match the target name
	- Note: All keys of the send OpenC2 Command will be arguments given to the registered target function
	- Note: If the OpenC2 Command key is not specified in the function arguments (as below), the kwargs argument will contain all extra nonepecified key word arguments as a dictionary format for use if needed
	- Note: The target function needs to return an OpenC2 formatted python dictionary

	- These functions are intended to be the processor of the OpenC2 Command and return an OpenC2 Response

	Matching target name register decorator
	
	```python
	...
	@ACTION.register
	def scan(act, *extra_args, **extra_kwargs):
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )
	...
	```
	
	Non-matching target name register decorator
	
	```python
	...
	@ACTION.register(key="scan")
	def example_scan(act, *extra_args, **extra_kwargs):
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )
	...
	```
	
	Matching target name register function
	
	```python
	...
	def scan(act, *extra_args, **extra_kwargs):
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )
    
    
	ACTION.register(scan)
	...
	```
	
	Non-matching target name register function
	
	```python
	...
	def example_scan(act, *extra_args, **extra_kwargs):
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )
    
    
	ACTION.register(example_scan, key="scan")
	...
	```
	
5. Repeat step 3 to add more targets, repeate step 2 and 3 to add more actions

6. In the `act_server/actions` folder is a file named `__init__.py`, the contents of the file should be edited acordingly
	- Repeat the line `from .action import ACTION` as needed
		- `action` is the name of the file
		- `ACTION` is the name of the Dispatch variable
		- Add the `ACTION` to the `__all__` list in quotes

	```python
	from .query import Query
	from .action import ACTION

	__all__ = [
	    "Query",
	    "ACTION"
	]
	```

7. In the`act_Server` directory in a file named `actuator.py`, the contents of the file should be editied accordingly
	- Replace and repeat `ACTION` with an action that in in the `__all__` list from `act_server/actions/__init__.py`
	- Repeat the line `self._dispatch.register_dispatch(ACTION)` and replace `ACTION` with an imported action from `actions`

	```python
    from sb_utils.actuator import ActuatorBase

	from .actions import (
	    Query,
	    ACTION
	)
	
	
	class Actuator(ActuatorBase):
	    def __init__(self, *args, **kwargs):
	        super(Actuator, self).__init__(*args, **kwargs)
	        self._dispatch.register_dispatch(Query)
	```

8. Add any additional, non-standard, python libraries used to the `requirements.txt` file in the root folder


## Running the Actuator
Actuator is configured to run a Docker container.

1. Install docker

2. Build/pull container
    - Build
		- Run the `configure.py` script in the parent folder to create the Dockerfiles for the actuators
		- Return to the actuator folder and run the following commands, replacing `ACTUATOR` with the name of the actuator in lowercase
    	
	    ```bash
	    docker build -f Dockerfile -t PATH:ACTUATOR .
	    ```

3. Start the container
    - Note: There should be a RabbitMQ and transport container/instance for the actuator to connect to

- Development
    - Note: To reload the actuator, restart the container
    
     ```bash
    docker run \
	--hostname slpf \
	--name slpf \
    -e QUEUE_HOST=queue \
    -e QUEUE_PORT=5672 \
    -e QUEUE_USER=guest \
    -e QUEUE_PASSWORD=guest \
    -e QUEUE_EXCHANGE=device \
    -e QUEUE_ACTUATOR_KEY=actuator \
    -v $(PWD)/act_server:/opt/actuator/act_server \
	--link queue \
	--rm \
    PATH:ACTUATOR
	```
    
- Production
    
    ```bash
     docker run \
	--hostname slpf \
	--name slpf \
    -e QUEUE_HOST=queue \
    -e QUEUE_PORT=5672 \
    -e QUEUE_USER=guest \
    -e QUEUE_PASSWORD=guest \
    -e QUEUE_EXCHANGE=device \
    -e QUEUE_ACTUATOR_KEY=actuator \
	--link queue \
	--rm \
    PATH:ACTUATOR
	```
