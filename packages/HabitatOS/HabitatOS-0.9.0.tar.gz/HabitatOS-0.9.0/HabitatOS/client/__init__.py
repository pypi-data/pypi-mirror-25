import json
import os
import http.client
import logging


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
log = logging.getLogger('habitatos-client')


class HabitatOSAbstractBaseClass:

    def __init__(self, config=None, debug=False):
        with open(config) as file:
            self.config = json.loads(file.read())

        self.url = self.config['url']
        self.username = self.config['username']
        self.password = self.config['password']
        self.debug = debug
        self._connection = None
        self._auth = None

    def _authenticate(self):
        raise NotImplementedError

    def _connect(self):
        raise NotImplementedError

    def _get_auth(self):
        if not self._auth:
            self._auth = self._authenticate()
        return self._auth

    def _get_connection(self):
        if not self._connection:
            self._connection = self._connect()
        return self._connection

    def _debug(self, data):
        if self.debug:
            log.debug('\n\n')
            http.client.HTTPConnection.debuglevel = 1
            log.debug(f'{data}\n\n')

    def _request(self, method='GET', path='/', data={}, headers={'Content-Type': 'application/json'}):
        url = f'{self.url}/api/v1{path}'
        auth = self._get_auth()
        connection = self._get_connection()
        self._debug(locals())
        return connection.request(method=method, url=url, data=data, headers=headers, auth=auth)

    def post(self, path='/', data={}, headers={}):
        return self._request('POST', path=path, data=data, headers={})

    def get(self, path='/', data={}, headers={}):
        return self._request('GET', path=path, data=data, headers={})

    def put(self, path='/', data={}, headers={}):
        return self._request('PUT', path=path, data=data, headers={})

    def head(self, path='/', data={}, headers={}):
        return self._request('HEAD', path=path, data=data, headers={})

    def delete(self, path='/', data={}, headers={}):
        return self._request('DELETE', path=path, data=data, headers={})


from .basic import HabitatOSBasicAuth
from .oauth import HabitatOSOAuth2
