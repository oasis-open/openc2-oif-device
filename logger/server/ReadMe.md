# Logger GUI
Simple python syslog server

## Notes:
- Listens on port 514 default, configurable
- Logs to file and ElasticSearch
- Caches logs if ElasticSearch cannot be found

# Container Env Vars
- HOST_PORT - port to listen for syslog - default '514'
- LOG_PREFIX - string ot prefix logs with - default 'logger'
- ES_HOST - host with ElasticSearch instance - default 'None'
- ES_PORT - port ElasticSearch is listening - default '9200'
- ES_TRIES - max attempts to connect to ElasticSearch in 1s intervals - default '60'


# Resources
- Based on [Gist from marcelom](https://gist.github.com/marcelom/4218010)