# OASIS TC Open: oif-logger

## Server

### About the Server Image

- This image is Alpine 3.10 with a simple syslog server for use with [Elasticsearch](https://hub.docker.com/_/elasticsearch)
- Listens on port 514 default, configurable
- Logs to file and ElasticSearch
- Caches logs if ElasticSearch cannot be found

### How to use the Server Image

Note: Pulling an image requires using a specific tag (server or gui), the latest tag is not supported.

Environment Variables

| Variable | Type | Description | Default|
| ----------- | ----------- | ----------- | ----------- |
| ES_HOST | String | Host/IP of the Elasticsearch node | es_logger
| ES_PORT | Integer | Port of the Elasticsearch Node | 9200
| LOG_PREFIX | String | Prefix for the index in the format of `log_{LOG_PREFIX}-{YYYY.mm.dd}`  | logger
| ES_TRIES | Integer | Max attempts to connect to ElasticSearch in 1s intervals | 60

### Server Resources

- Based on [Gist from marcelom](https://gist.github.com/marcelom/4218010)

## GUI

### About the GUI Image

- This image is Alpine 3.10 with a simple GUI for use with [Elasticsearch](https://hub.docker.com/_/elasticsearch)
- UI port - 8081

### How to use the GUI Image

Note: Pulling an image requires using a specific tag (server or gui), the latest tag is not supported.

Environment Variables

| Variable | Type | Description | Default|
| ----------- | ----------- | ----------- | ----------- |
| ES_HOST | String | Host/IP of the Elasticsearch node | es_logger
| ES_PORT | Integer | Port of the Elasticsearch Node | 9200

### GUI Resources

- [Lodash](https://www.npmjs.com/package/lodash) - Lodash library for node
- [Moment](https://www.npmjs.com/package/moment) - DateTime formatting/parsing
- [Query String](https://www.npmjs.com/package/query-string) - Parse and stringify URL query strings
- [React](https://reactjs.org/) - Core Framework
  - [DOM](https://www.npmjs.com/package/react-dom)
  - [Moment](https://www.npmjs.com/package/react-moment) - Date/Time Formatting
  - [Base Scripts](https://www.npmjs.com/package/react-scripts)
- [Reactstrap](https://www.npmjs.com/package/reactstrap) - Bootstrap v4 components for React
- [SearchKit](http://www.searchkit.co/) - ElasticSearch UI components
- [SearchKit DateFilter](https://www.npmjs.com/package/searchkit-datefilter)
