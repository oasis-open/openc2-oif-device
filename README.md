<a id="openc2-logo" href="https://openc2.org/" target="_blank">![OpenC2](https://github.com/ScreamBun/SB_Utils/blob/master/assets/images/openc2.png?raw=true)</a>

# <a name="oasis-tc-open-repository:-openc2-oif-device"></a> OASIS TC Open Repository: openc2-oif-device

### <a name="openc2-integration-framework-(oif)-device"></a> <i>OpenC2 Integration Framework (OIF) Device</i>

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-yellow)](https://www.python.org/downloads/release/python-3100/)
[![Docker 18.0+](https://img.shields.io/badge/Docker-18.0%2B-blue)](https://docs.docker.com/get-docker/)
[![OpenC2 Lang Spec](https://img.shields.io/badge/OpenC2%20Lang%20Spec-1.0-brightgreen)](https://openc2.org/specifications)

# OIF Device

The OIF Device provides an example of an OpenC2 Consumer, which has the potential to easily interoperate with other entities and functions and then, provide an OpenC2 Response.  
The OIF Device supports JSON encoding of OpenC2 commands and responses, and message transfer over MQTT or HTTP.

Given OpenC2's goals and design philosphy, the Consumer implementer essentially should:

1) Interface to the message fabric to receive commands and send responses
2) Receive commands and validate them against the relevant AP schema
3) Parse the command and convert / translate / interpret into the local syntax / API for the relevant function
4) Execute the commanded action, and collect response information
5) Package the response information in OpenC2 format
6) Send the response back to the Producer (or other destination, per the environment)

OIF Device provides a skeleton for steps 3 and 4, but only a very basic implementation as a starting point.

Basic support for two OpenC2 APs is provided; either can be enabled within the config.toml file via the following configuration fields:

- schema_file: Actuator Profile to be used for message validation
  - options are [th_ap_vbeta.json or slpf_ap_v2.0.json]
- HTTP / is_enabled: HTTP transport functionality.  Enabled by default.
- MQTT / is_enabled: MQTT transport functionality.  Enabled by default.
- KESTREL / is_enabled: Kestrel exmample queiries.  Disabled by default.
- SLPF: Feature Flag comming soon, explicidly on by default.

Various other configurations are available from the config.toml file.  The application will need to be bounced if a change is applied.

The examples provided with OIF Device are not intended for production use.

## <a name="background"></a> Background

This GitHub public repository [openc2-oif-device](https://github.com/oasis-open/openc2-oif-device) was created at the request of the [OASIS OpenC2 Technical Committee](https://www.oasis-open.org/committees/openc2/) as an [OASIS TC Open Repository](https://www.oasis-open.org/resources/open-repositories/) to support development of open source resources related to Technical Committee work.

While this TC Open Repository remains associated with the sponsor TC, its development priorities, leadership, intellectual property terms, participation rules, and other matters of governance are separate and distinct from the OASIS TC Process and related policies.

All contributions made to this TC Open Repository are subject to open source license terms expressed in [Apache License v 2.0](https://www.oasis-open.org/sites/www.oasis-open.org/files/Apache-LICENSE-2.0.txt). That license was selected as the declared [Applicable License](https://www.oasis-open.org/resources/open-repositories/licenses) when the TC voted to create this Open Repository.

As documented in [Public Participation Invited](https://github.com/oasis-open/openc2-oif-device/blob/master/CONTRIBUTING.md#public-participation-invited), contributions to this TC Open Repository are invited from all parties, whether affiliated with OASIS or not. Participants must have a GitHub account, but no fees or OASIS membership obligations are required.  Participation is expected to be consistent with the [OASIS TC Open Repository Guidelines and Procedures](https://www.oasis-open.org/policies-guidelines/open-repositories), the open source [LICENSE.md](LICENSE.md) designated for this particular repository, and the requirement for an [Individual Contributor License Agreement](href="https://www.oasis-open.org/resources/open-repositories/cla/individual-cla) that governs intellectual property.

## <a id="purposeStatement"></a> Statement of Purpose

OpenC2 Integration Framework (OIF) is a project that will enable developers to create and test OpenC2 specifications and implementations without having to recreate an entire OpenC2 ecosystem.

OIF consists of two major parts. The "orchestrator" which functions as an OpenC2 producer and the "Device" which functions as an OpenC2 consumer.

This particular repository contains the code required to set up an OpenC2 Device. The Orchestrator repository can be found [here](https://github.com/oasis-open/openc2-oif-orchestrator). Due to port bindings it is recommended that the orchestrator and the device not be run on the same machine.

The OIF Device was created with the intent of being an easy-to-configure OpenC2 consumer that can be used in the creation of reference implementations. To that end it allows for the addition of multiple actuators, serializations, and transportation types.

## <a name="overview"></a> Overview

![GUI snippet](assets/oif_overview.png)

## General Setup & Start

- Clone from git
- Create a virtual environment
- Run: `pip install -r requirements.txt`
- Run: `python ./main.py`
- Go here to view the HTTP APIs: `http://127.0.0.1:5000/docs`
- See the config.toml file for MQTT Topics and to enable features

***Note:** See below to setup more advanced capabilities, such as Kestrel STIX Shifter and Elastic.***

## Kestrel Elasticsearch and Kibana Setup

Clean your docker instances:

```bash
./scripts/cleanup.sh
```

Start the Elastic and Kibana Network, run:

```bash
docker network create elastic
```

Start Elastic with SSL/HTTPS (Elastic uses this by default)

Create docker:

```bash
docker run \
      --name elasticsearch \
      --net elastic \
      -p 9200:9200 \
      -e discovery.type=single-node \
      -e ES_JAVA_OPTS="-Xms1g -Xmx1g"\
      -e ELASTIC_PASSWORD=elastic \
      -it \
      docker.elastic.co/elasticsearch/elasticsearch:8.2.2
```

In another terminal, get Elastic's CA Cert to login and make calls later:

```bash
docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

To see if Elastic's CA Cert was obtained successfully:

```bash
curl --cacert http_ca.crt https://elastic:elastic@localhost:9200
```

Should be similar:

```json
{
  "name" : "b560471008eb",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "GRzNb8kdTXW54T1KLMQBFA",
  "version" : {
    "number" : "8.2.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "9876968ef3c745186b94fdabd4483e01499224ef",
    "build_date" : "2022-05-25T15:47:06.259735307Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

Start Kibana docker instance, run:

```bash
docker run \
    --name kibana \
    --net elastic \
    -p 5601:5601 \
    docker.elastic.co/kibana/kibana:8.2.2
```

Should be similar (code may be different):

```bash
Login to Kibana with security token by opening the given link in a web browser:

http://0.0.0.0:5601/?code=038409 
```

In a new terminal, get the **Enrollment token**:

```bash
docker exec -it elasticsearch \
    /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token \
    -s kibana
```

Login to Kibana

- elastic
- elastic

Load Data into ElasticSearch, run (only needed once):

```bash
 npm i elasticdump -g 
 ```

Then, run:

```bash
./scripts/load-elastic-data.sh 
```

Output:

```bash
Mon, 05 Jun 2023 13:46:55 GMT | dump complete
```

## View Data in KibanaGuide

### View Data

 On the side navigation bar, go to **Management > Stack Management > Index Management** to view the Indices. This will show you the data stored in the Elasticsearch.

### Execute Queries

- On the side navigation bar, go to **Management > DevTools** to do raw queries similar to HTTP GET requests or curl requests
- On the side navigation bar, go to **Analytics > Dashboard** and create a DataView to query the data using a UI

## Sample queries

### Kibana DevTools

```json
GET /linux-91-sysflow-bh22-20220727/_search?size=1
{
  "query": {
    "query_string": {
      "query": "0.4.3",
      "fields": [
        "agent.version"
      ]
    }
  }
}
```

### Curl

```bash
curl --cacert ./http_ca.crt  "https://elastic:elastic@localhost:9200/linux-91-sysflow-bh22-20220727/_search?size=1"
```

#### To get Pretty Print

- Add to your ~/.bashrc file:
  `
  alias pp='python -mjson.tool'
  `
- `source ~/.bashrc`
- Add `| pp` to the end of your cmdl query

```bash
curl --cacert ./http_ca.crt -XGET "https://elastic:elastic@localhost:9200/linux-91-sysflow-bh22-20220727/_search?size=1" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -d'
{
  "query": {
    "query_string": {
      "query": "0.4.3",
      "fields": [
        "agent.version"
      ]
    }
  }
}' | pp
```

## Kicking off a Kestrel Hunt

### Setup Kestrel

Install dependencies

```bash
pip install -r requirements.txt
```

To test, run:

```bash
kestrel ./hunts/huntflow/helloworld.hf
```

**Output**

```bash
name pid
firefox.exe 201
 chrome.exe 205

[SUMMARY] block executed in 1 seconds
VARIABLE    TYPE  #(ENTITIES)  #(RECORDS)  process*
proclist process            4           4         0
browsers process            2           2         0
*Number of related records cached.
```

### Run the STIXShifter Hunt on Elastic

<sup>Preloaded and mapped data</sup>

To setup the configuration file, see: [STIX-shifter Data Source Interface](https://kestrel.readthedocs.io/en/stable/source/kestrel_datasource_stixshifter.interface.html)

```bash
kestrel ./hunts/huntflow/query_data_via_stixshifter.hf
```

### Run STIX Bundle Hunts on JSON files

<sup>STIX formatted data</sup>

From an https github file

```bash
kestrel ./hunts/huntflow/helloworld.hf
```

From a local file (Need script to pass in path to file, hardcoded)

```bash
kestrel ./hunts/huntflow/query_local_stixdata.hf
```

```bash
kestrel ./hunts/huntflow/query_net_traffic_stixdata.hf
```

## References

- [How to run Elasticsearch 8 on Docker for Local Development](https://levelup.gitconnected.com/how-to-run-elasticsearch-8-on-docker-for-local-development-401fd3fff829)

- [Kestrel's Hunting Stack Testing](https://github.com/opencybersecurityalliance/hunting-stack-testing/blob/main/scripts/)
