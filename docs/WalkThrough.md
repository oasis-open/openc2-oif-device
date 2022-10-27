# <a name="openC2-integration-framework-(oif)-device-walk-through"></a> OpenC2 Integration Framework (OIF) Device Walk Through

This document provides a detailed walk through of the installation, configuration, and startup of the OIF
Device. The OIF Device implements the OASIS OpenC2
[Consumer](https://docs.oasis-open.org/openc2/oc2ls/v1.0/cs02/oc2ls-v1.0-cs02.html#16-overview) functionality.

Important note, an OIF Device must be coupled with an OIF Orchestrator.  The OIF Orchestrator contains a GUI, 
which will allow the user to register the OIF Device, create actuators, etc.   See the OIF Orchestrator 
[Readme](https://github.com/oasis-open/openc2-oif-orchestrator) and 
[Walk Through](https://github.com/oasis-open/openc2-oif-orchestrator/blob/master/docs/WalkThrough.md) documentation 
if you have not already set up an OIF Orchestrator.   

## 1) System Preparation
 - Required:  
   - [Python 3.10+](https://www.python.org/)
     - [pip 18+](https://pip.pypa.io/en/stable/)
   - [Docker 18.0+](https://www.docker.com/)
     - [Docker Compose 1.20+](https://docs.docker.com/compose/)
 - Optional: 
   - [Git Latest Version](https://git-scm.com/)

[Pip](https://pip.pypa.io/en/stable/) and [Docker
Compose](https://docs.docker.com/compose/)
are needed for configuration and startup.  Pip is usually [installed with
Python](https://pip.pypa.io/en/stable/installing/). Docker Compose is [installed with
Docker](https://docs.docker.com/compose/install/) on Windows
and Mac systems, but must be installed separately on Linux
systems.  If using a Linux environment, then the [post-installation steps for
Linux](https://docs.docker.com/engine/install/linux-postinstall/) are also needed,
specifically:

 * Manage Docker as a non-root user
 * Configure Docker to start on boot

Users are advised to update all the software components to the latest versions.

Users may optionally install [git](https://git-scm.com/) version control software, as a means of obtaining the OIF
Device software.

## 2) Obtain the Software

There are two approaches to obtain the software, clone via git or download using ZIP:
 1. Clone the [OIF Device Repository](https://github.com/oasis-open/openc2-oif-device) in the desired location:<br>
    `git clone https://github.com/oasis-open/openc2-oif-device.git`
 1. Download a ZIP archive by 
    1. Navigating to the [OIF Device Repository](https://github.com/oasis-open/openc2-oif-device).
	1. Click on the green **Code** button.
	1. Select **Download ZIP**.
	1. Unwrap the ZIP archive in the desired location.

## 3) Configuration 

To configure the OIF Device, navigate to the directory containing the local software copy 
and run `configure.py` with the desired options prior to starting the OIF Device for the first time.

View all configuration options:
```bash 
python3 configure.py -h
```

Run with default configuration:
```bash 
python3 configure.py
```

Run with logging to the designated file and in verbose mode:
```bash 
python3 configure.py -f FILE -v
```

## 3) Run the OIF Device

As described in [its documentation](https://docs.docker.com/compose/), Docker Compose is used to 
"define and run multi-container Docker applications". To start OIF Device in its default
configuration, the only required command is:

```bash
docker-compose -f device-compose.yaml up
```

This command will:
 - Create the necessary Docker images as defined in the `device-compose.yml` configuration file
 - Execute the application in the defined containers, attached to the terminal from which it was launched  

Execution of an attached OIF instance is terminated by typing `ctrl-c` in the terminal.

The OIF Device can also be started in detached mode using the docker-compose `-d` or `--detach` option:

```bash
docker-compose -f device-compose.yaml up --detach
```

A detached instance of OIF Device is terminated with the complementary command:

```bash
docker-compose -f device-compose.yaml down
```

This command should also be run after terminating an attached OIF Device instance with `ctrl-c`, 
as it also performs a number of desirable clean-up actions.

[Top of Page](#openC2-integration-framework-(oif)-device-walk-through)