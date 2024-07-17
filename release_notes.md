# OpenC2 Device Release Notes

## v2.2.0
* Updated a number of vulnerable dependencies
* Bumped jinja2 from 3.13 to 3.14
* Bumped setuptols from 68.0.0 to 70.0.0
* Bumped express from 4.18.2 to 4.19.2
* Fixed stix2-validator version to 3.1.4 

## v2.1.0

* Revamped MQTT connection logic
* Updated HTTP logic
* Introduced Feature Flags, to allow extra features to be easily enabled or disabled from the config.toml file
* Kestrel logic is included but Feature Flagged Off
* Improved device client id generation
* Improved OpenC2 command validation
* Introduced the Threat Hunt Schema
* Bumped express from 4.18.2 to 4.19.2 in /node_utils
* Bumped fastapi from 0.100.0 to 0.110.0
* Bumped jinja2 from 3.1.2 to 3.1.3

## v2.0.0

* Major improvements to the http and mqtt transports
* Includes the beta threat hunting actuator profile for message validation
* Streamlined startup
* Introduction of configurable features via the config.toml
* Basic kestrel integration examples
* Updated readme documentation with clearer instructions, examples and OpenC2 goals
