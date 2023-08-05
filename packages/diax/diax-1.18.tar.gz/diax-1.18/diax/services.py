import json
import logging

import diax.errors
import ramlfications
import requests

LOGGER = logging.getLogger(__name__)

def _to_resource_name(uri):
    "Convert a resource uri like '/foo/bar/' to a name like foo.bar"
    if uri[0] == '/':
        uri = uri[1:]
    if uri[-1] == '/':
        uri = uri[:-1]
    parts = uri.split('/')
    valid = [p for p in parts if p != '{uuid}']
    return '.'.join(valid)

class Service():
    def __init__(self, client, name):
        self.baseUri        = None
        self.client         = client
        self.documentation  = None
        self.media_type     = None
        self.name           = name
        self.options        = None
        self.resources      = {}
        self.title          = None

    def load(self):
        try:
            response = self.client.options(self.name, '/')
        except diax.errors.RequestError as e:
            LOGGER.error("Failed to load up RAML for %s: %s", self.name, e)
            return
        raml = ramlfications.loads(response)
        for k in ('baseUri', 'documentation', 'mediaType', 'title', 'version'):
            setattr(self, k, raml.pop(k, None))
        for relativeUri, resource in raml.items():
            resource_name = _to_resource_name(relativeUri)
            if resource_name not in self.resources:
                self.resources[resource_name] = Resource(self, relativeUri)
            self.resources[resource_name].add(resource)

    def __getitem__(self, name):
        try:
            return self.resources[name]
        except KeyError:
            LOGGER.warning("Unable to find resource %s in service %s. Attempting to fake one...", name, self.name)
            return Resource(self, '/{}/'.format(name))

class Resource():
    def __init__(self, service, uri):
        self.methods = {}
        self.service = service
        self.uri     = uri

    def add(self, schema):
        for k, v in schema.items():
            if k not in ('delete', 'get', 'options', 'patch', 'post', 'put'):
                continue
            self.methods[k] = Method(v)

    def post(self, payload):
        try:
            self.methods['post'].validate(payload)
        except KeyError:
            LOGGER.warning("Can't validate paramters")
        _, headers = self.service.client.post(self.service.name, self.uri, payload)
        return headers['Location']

    def list(self):
        data = self.service.client.get(self.service.name, self.uri)
        return data

class Method():
    def __init__(self, schema):
        self.schema = None
        for content_type, descriptor in schema.get('body', {}).items():
            if not (content_type == 'application/json' and 'schema' in descriptor):
                continue
            self.schema = json.loads(descriptor['schema'])

    def validate(self, payload):
        errors = []
        for k in self.schema['required']:
            if k not in payload:
                errors.append("The parameter '{}' is required".format(k))
        if errors:
            raise diax.errors.ValidationError("\n".join(errors))

def connect(client, name):
    "Connect to the given service, pull down the definition of its endpoints"
    service = Service(client, name)
    service.load()
    return service
