import os
import time
import logging
import socket
import yaml
import re

import pymongo
import requests
import pandas as pd
from tornado import ioloop, web, httpserver, process

from factornado.handlers import Info, Heartbeat, Swagger, Log


class Kwargs(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)


class WebMethod(object):
    def __init__(self, method, url, logger=None):
        self.logger = logger if logger is not None else logging.root
        self.method = method
        self.url = url
        self.params = re.findall("{(.*?)}", self.url)
        self.__doc__ = (
            '\nParameters\n----------\n' +
            '\n'.join(["{} : str".format(x) for x in self.params]))

    def __call__(self, data='', headers=None, **kwargs):
        url = self.url.format(**kwargs)
        response = requests.request(
            method=self.method,
            url=url,
            data=pd.io.json.dumps(data),
            headers=headers if headers is not None else {},
            )
        try:
            response.raise_for_status()
        except Exception as e:
            reason = '{} {} > {}'.format(self.method, url, response.reason)
            raise web.HTTPError(response.status_code, reason, reason=reason)
        return response


class Callback(object):
    def __init__(self, application, uri, sleep_duration=0, method='post'):
        self.application = application
        self.uri = uri
        self.sleep_duration = sleep_duration
        self.method = method

    def __call__(self):
        self.application.logger.debug('{} callback started'.format(self.uri))
        url = 'http://localhost:{}/{}'.format(self.application.get_port(), self.uri.lstrip('/'))
        response = requests.request(self.method, url)
        try:
            response.raise_for_status()
        except Exception as e:
            reason = '{} {} > {}'.format(
                self.method, url, response.reason)
            raise web.HTTPError(response.status_code, reason, reason=reason)
        if response.status_code != 200:
            self.application.logger.debug('{} callback returned {}. Sleep for a while.'.format(
                self.uri, response.status_code))
            time.sleep(self.sleep_duration)
        self.application.logger.debug('{} callback finished : {}'.format(self.uri,
                                                                         response.text))


class Application(web.Application):
    def __init__(self, config, handlers, logger=None, **kwargs):
        self.config = config if isinstance(config, dict) else yaml.load(open(config))
        self.handler_list = [
            ("/swagger.json", Swagger),
            ("/swagger", web.RedirectHandler, {'url': '/swagger.json'}),
            ("/heartbeat", Heartbeat),
            ("/log", Log),
            ("/info", Info),
            ] + handlers
        super(Application, self).__init__(self.handler_list, **kwargs)

        # Set logging config
        if logger is None:
            logging.basicConfig(
                level=self.config['log']['level'],  # Set to 10 for debug.
                filename=self.config['log']['file'],
                format='%(asctime)s (%(filename)s:%(lineno)s)- %(levelname)s - %(message)s',
                )
            logging.Formatter.converter = time.gmtime
            logging.getLogger('requests').setLevel(logging.WARNING)
            logging.getLogger('tornado').setLevel(logging.WARNING)
            self.logger = logging.root
        else:
            self.logger = logger

        # Create mongo attribute
        self.mongo = Kwargs()
        _mongo = self.config.get('db', {}).get('mongo', {})
        self.mongo = Kwargs(**{
            collname: pymongo.MongoClient(host['address'],
                                          connect=False)[db['name']][coll['name']]
            for hostname, host in _mongo.get('host', {}).items()
            for dbname, db in _mongo.get('database', {}).items() if db['host'] == hostname
            for collname, coll in _mongo.get('collection', {}).items() if coll['database'] == dbname
            })

        # Create service attribute
        self.services = Kwargs(**{
            key: Kwargs(**{
                subkey: Kwargs(**{
                    subsubkey: WebMethod(
                        subsubkey,
                        self.config['registry']['url'].rstrip('/')+subsubval,
                        logger=self.logger,
                        )
                    for subsubkey, subsubval in subval.items()})
                for subkey, subval in val.items()
                })
            for key, val in self.config.get('services', {}).items()})

    def get_port(self):
        if 'port' not in self.config:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            self.config['port'] = s.getsockname()[1]
            s.close()
        return self.config['port']

    def get_host(self):
        if 'host' not in self.config:
            self.config['host'] = socket.gethostname()
        return self.config['host']

    def start_server(self):
        self.logger.info('='*80)

        port = self.get_port()  # We need to have a fixed port in both forks.
        self.logger.info('Listening on port {}'.format(port))
        if os.fork():
            server = httpserver.HTTPServer(self)
            server.bind(self.get_port(), address=self.config.get('ip', '0.0.0.0'))
            server.start(self.config['threads_nb'])
            ioloop.IOLoop.current().start()
        elif os.fork():
            time.sleep(2)  # We sleep for a few seconds to let the registry start.
            # Send a heartbeat callback
            cb = Callback(self, '/heartbeat', sleep_duration=0, method='post')
            cb()
        else:
            time.sleep(2)  # We sleep for a few seconds to let the registry start.
            if self.config.get('callbacks', None) is not None:
                for key, val in self.config['callbacks'].items():
                    if os.fork():
                        if val['threads']:
                            process.fork_processes(val['threads'])
                            ioloop.PeriodicCallback(
                                Callback(self, val['uri'],
                                         sleep_duration=val.get('sleep', 0),
                                         method=val.get('method', 'post'),
                                         ),
                                val['period']*1000).start()
                            ioloop.IOLoop.instance().start()

    def stop_server(self):
        ioloop.IOLoop.current().stop()
