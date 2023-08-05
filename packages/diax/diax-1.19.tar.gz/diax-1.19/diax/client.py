import json
import logging
import os
import pprint
import requests
import urllib
import yaml

import diax.errors
import diax.uri

LOGGER = logging.getLogger(__name__)

CREDENTIALS_FILE = os.path.join(os.environ['HOME'], '.authentise', 'credentials')
class Client():
    def __init__(self, environment, impersonate=None, internal_token=None, password=None, ssl_verify=True, username=None,):
        self.environment    = environment
        self.impersonate    = impersonate
        self.internal_token = internal_token
        self.password       = password
        self.session        = requests.Session()
        self.ssl_verify     = ssl_verify
        self.username       = username

    def _do_login(self):
        if self.internal_token:
            LOGGER.info("No login necessary, using internal token")
            self.session.auth = ('api', self.internal_token)
            return
        payload = {
            'password'  : self.password,
            'username'  : self.username,
        }
        _, headers = self.post('users', '/sessions/', payload)
        LOGGER.debug("Got headers from login: %s", pprint.pformat(headers.items()))

    def _auth(self):
        if self.internal_token:
            return ('api', self.internal_token)
        else:
            return None

    def _ensure_has_credentials(self):
        if self.internal_token:
            LOGGER.info("Using internal token")
            return
        if self.username and self.password:
            LOGGER.debug("Using credentials provided via commandline")
            return
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                data = yaml.load(f)
            credentials = data.get(self.environment)
            if not credentials:
                raise diax.errors.CredentialsError("You have a {} file but it needs a section for environment {}".format(CREDENTIALS_FILE, self.environment))
            self.password = credentials.get('password')
            self.username = credentials.get('username')
            if not self.username:
                raise diax.errors.CredentialsError("You have a section in {} for environment {} but it doesn't have a username".format(CREDENTIALS_FILE, self.environment))
            if not self.password:
                raise diax.errors.CredentialsError("You have a section in {} for environment {} but it doesn't have a password".format(CREDENTIALS_FILE, self.environment))
            return
        raise diax.errors.CredentialsError("You need to either specify credentials on the commandline with -u and -p or you need to create a credentials file at {}".format(CREDENTIALS_FILE))

    def _get_user_uri(self, username):
        results = self.list('users', '/users/', filters={'username': username})
        if results:
            return results[0]['uri']

    def _maybe_impersonate(self):
        if not self.impersonate:
            return
        LOGGER.debug("Impersonating %s", self.impersonate)
        uri = self.impersonate if diax.uri.is_uri(self.impersonate, 'users', '/users/') else self._get_user_uri(self.impersonate)
        if not uri:
            raise diax.errors.ImpersonationError("The value '{}' is not a user URI or username".format(self.impersonate))
        payload = {
            'impersonating' : uri,
        }
        self.put('users', '/sessions/0/', payload)

    def _validate(self, response, method, url):
        if not response.ok:
            LOGGER.debug("Response body: %s", response.text)
            raise diax.errors.RequestError(method, url, response)
        if response.status_code == 204 or response.status_code == 201:
            return None, response.headers
        try:
            return response.json(), response.headers
        except ValueError:
            return response.text, response.headers

    def get(self, service, path, filters={}):
        url = self.url(service, path, filters)
        response = self.session.get(url, verify=self.ssl_verify)
        out, _ = self._validate(response, 'GET', url)
        return out

    def list(self, service, path, filters={}):
        result = self.get(service, path, filters=filters)
        return result['resources']

    def login(self):
        self._ensure_has_credentials()
        self._do_login()
        self._maybe_impersonate()

    def options(self, service, path):
        url = self.url(service, path)
        response = self.session.options(url, verify=self.ssl_verify)
        out, _ = self._validate(response, 'OPTIONS', url)
        return out

    def post(self, service, path, payload):
        url = self.url(service, path)
        response = self.session.post(url, json=payload, verify=self.ssl_verify, auth=self._auth())
        out, headers = self._validate(response, 'POST', url)
        return out, headers

    def put(self, service, path, payload):
        url = self.url(service, path)
        response = self.session.put(url, json=payload, verify=self.ssl_verify)
        out, _ = self._validate(response, 'PUT', url)
        return out

    def rawdelete(self, url):
        response = self.session.delete(url, verify=self.ssl_verify)
        out, _ = self._validate(response, 'DELETE', url)
        return out

    def rawpost(self, url, payload, headers=None):
        response = self.session.post(url, json=payload, verify=self.ssl_verify, headers=headers)
        _, headers = self._validate(response, 'POST', url)
        return headers

    def rawput(self, url, payload, headers=None):
        response = self.session.put(url, json=payload, verify=self.ssl_verify, headers=headers)
        out, _ = self._validate(response, 'PUT', url)
        return out

    def rawget(self, url):
        return self._validate(self.session.get(url, verify=self.ssl_verify, auth=self._auth()), 'GET', url)

    def url(self, service, path, filters=None):
        base_pattern = "{{}}.{}".format(self.environment) if "{}" not in self.environment else self.environment
        base = base_pattern.format(service)
        _url = "https://{}{}".format(base, path)
        queryargs = {}
        filters = filters or {}
        queryargs.update({'filter[{}]'.format(k): v for k, v in filters.items()})
        if queryargs:
            _url += '?' + urllib.parse.urlencode(queryargs)
        return _url

    def streamevents(self):
        _url = self.url('events', '/')
        response = self.session.get(_url, stream=True, verify=self.ssl_verify)
        if not response.ok:
            raise diax.errors.RequestError('GET', _url, response)
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                yield json.loads(line)

def create(args):
    "Create a client to talk to 3DIAX with the specified environment"
    return Client(
        environment         = args.environment,
        impersonate         = args.impersonate,
        internal_token      = args.internal_token,
        ssl_verify          = args.certificate_bundle or not args.ssl_no_verify,
        password            = args.password,
        username            = args.username,
    )

