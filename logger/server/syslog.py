#!/usr/bin/env python
import logging
import os
import time
import urllib3

from datetime import datetime, timezone
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from logging.handlers import RotatingFileHandler
from syslog_rfc5424_parser import SyslogMessage, ParseError
# https://github.com/EasyPost/syslog-rfc5424-parser

try:
    from queue import Queue
except ImportError:
    import Queue

# Testing
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall

# Based on - https://gist.github.com/marcelom/4218010


# Object Dict
class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        self._hash = None
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.get(item, None)


"""
Tiny Syslog Server in Python.

This is a tiny syslog server that is able to receive UDP based syslog
entries on a specified port and save them to a file.
That's it... it does nothing else...
There are a few configuration parameters.
"""

# Generic Config
reactor.singleton = ObjectDict(
    DEFAULT_LOG='syslog.log',
    HOST="0.0.0.0",
    UDP_PORT=514,
    HOST_PORT=os.environ.get('HOST_PORT', 514),
    LOG_DIR=os.path.join('/', 'var', 'log', 'syslog'),
    # NO USER SERVICEABLE PARTS BELOW HERE...
    COUNT=ObjectDict(
        RECEIVED=0,
        PROCESSED=0,
        FORWARDED=0
    ),
    LOG_COUNT=0,
    LOG_PREFIX=os.environ.get('LOG_PREFIX', 'logger'),
    # ElasticSearch Config
    ES=ObjectDict(
        HOST=os.environ.get('ES_HOST', None),
        PORT=os.environ.get('ES_PORT', '9200'),
        RETRIES=os.environ.get('ES_TRIES', 60),
        QUEUE=Queue(),
        CONN=None
    ),
    APP_LOGS={},
    LOG_LEVELS=dict(
        crit=logging.CRITICAL,
        err=logging.ERROR,
        warn=logging.WARNING,
        info=logging.INFO,
        debug=logging.DEBUG,
        notset=logging.NOTSET
    )
)


def openLog(app):
    tmp_log = logging.getLogger(app)
    tmp_log.setLevel(logging.DEBUG)
    LOG_NAME = f'{app}.log' if app.startswith(f'{reactor.singleton.LOG_PREFIX}_') else f'{reactor.singleton.LOG_PREFIX}_{app}.log'

    handler = RotatingFileHandler(os.path.join(reactor.singleton.LOG_DIR, LOG_NAME), maxBytes=1024*20, backupCount=5)
    tmp_log.addHandler(handler)
    reactor.singleton.APP_LOGS[app] = tmp_log


def connectElasticsearch():
    ES = reactor.singleton.ES

    if ES.HOST is not None:
        while ES.RETRIES > 0:
            try:
                http = urllib3.PoolManager()
                rsp = http.request('GET', f'{ES.HOST}:{ES.PORT}', retries=False, timeout=1.0)
                print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - Connected to ElasticSearch at {ES.HOST}:{ES.PORT}')
                break

            except Exception:
                print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - ElasticSearch at {ES.HOST}:{ES.PORT} not up')
                ES.RETRIES -= 1
                time.sleep(1)

        if ES.RETRIES > 0:
            ES_CONN = Elasticsearch(f'{ES.HOST}:{ES.PORT}')
            while True:
                if not ES.QUEUE.empty():
                    msg = ES.QUEUE.get()
                    try:
                        rsp = ES_CONN.index(**msg)
                        reactor.singleton.COUNT.FORWARDED += 1

                    except (TransportError, Exception) as e:
                        print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - Log Error: {e}')
                        ES.QUEUE.put(msg)

                else:
                    time.sleep(1)
        else:
            print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - ElasticSearch at {ES.HOST}:{ES.PORT} not up, max retries reached')
            reactor.singleton.ES.HOST = None
            while not ES.QUEUE.empty():
                msg = ES.QUEUE.get()
                time.sleep(0.5)


class SyslogUDPHandler(DatagramProtocol):
    def datagramReceived(self, data, addr):
        data = bytes.decode(data.strip())

        try:
            message = SyslogMessage.parse(data).as_dict()
            message['hostname'] = reactor.singleton.LOG_PREFIX
            msg = message.get('msg', None)

            if msg not in ['', ' ', None]:
                reactor.singleton.COUNT.RECEIVED += 1
                appName = message.get('appname', 'default')
                level = message.get('severity', 'info')

                if appName not in reactor.singleton.APP_LOGS:
                    openLog(appName)

                log_msg = f"{message.get('timestamp', datetime.now())} - {level} - {msg}"
                reactor.singleton.APP_LOGS[appName].log(reactor.singleton.LOG_LEVELS.get(level), log_msg)
                reactor.singleton.COUNT.PROCESSED += 1

                if reactor.singleton.ES.HOST is not None:
                    reactor.singleton.ES.QUEUE.put(dict(
                        index=f'log_{reactor.singleton.LOG_PREFIX}-{datetime.now():%Y.%m.%d}',
                        doc_type='log',
                        body=message
                    ))

        except ParseError as e:
            print(f"Error {e.__class__.__name__} - {getattr(e, 'message', e)}")


def stats():
    COUNT = reactor.singleton.COUNT
    print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - Received {COUNT.RECEIVED:,}, Processed {COUNT.PROCESSED:,}, Forwarded {COUNT.FORWARDED:,}')


if __name__ == "__main__":
    for log in os.listdir(reactor.singleton.LOG_DIR):
        name, ext = os.path.splitext(log)
        if ext == '.log':
            openLog(name)

    if 'default' not in reactor.singleton.APP_LOGS:
        openLog('default')

    print(f'Syslog UDP Listening {reactor.singleton.HOST}:{reactor.singleton.HOST_PORT}')

    udpServer = SyslogUDPHandler()
    reactor.listenUDP(reactor.singleton.UDP_PORT, udpServer)

    reactor.callInThread(connectElasticsearch)

    status = LoopingCall(stats)
    status.start(60)

    try:
        reactor.run()
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print(f'{datetime.now(timezone.utc):%Y.%m.%d %H:%M:%S%z} - Crtl+C Pressed. Shutting down.')
