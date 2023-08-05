import aiohttp
import asyncio
import async_timeout
import json
import logging
import ssl

import diax.client
import diax.errors

LOGGER = logging.getLogger(__name__)

class AsyncClient(diax.client.Client):
    def __init__(self, *args, certificate_bundle=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.certificate_bundle = certificate_bundle
        # We can't create the session here because we'll get a lot message
        # about it not being inside a coroutine, even though it's synchronous
        self.session = None

    async def streamevents(self):
        url = self.url('events', '/')
        buffer_ = b''
        while True:
            try:
                LOGGER.info("Connecting to %s", url)
                async with self.session.get(url) as response:
                    while True:
                        buffer_ += await response.content.read(256)
                        try:
                            text = buffer_.decode('utf-8')
                        except ValueError:
                            LOGGER.debug("Failed to decode event buffer as UTF-8, waiting for more")
                            continue
                        if '\n' not in text:
                            LOGGER.debug("Failed to find \\n in %s, waiting for more", buffer_)
                            continue
                        datagram = text[:text.index('\n') + 1]
                        datagram_bytes = datagram.encode('utf-8')
                        LOGGER.debug("Found %s bytes of message data in %s bytes buffer", len(datagram_bytes), len(buffer_))
                        buffer_ = buffer_[len(datagram_bytes):]
                        await json.loads(datagram)
            except asyncio.TimeoutError as e:
                LOGGER.warning("Error streaming events: %s", e)

    async def _ensure_session(self):
        if not self.session:
            if self.certificate_bundle:
                context = ssl.create_default_context(
                    cafile  = self.certificate_bundle
                )
                connector = aiohttp.TCPConnector(ssl_context=context)
            else:
                connector = aiohttp.TCPConnector()
            kwargs = {'connector': connector}
            if self.internal_token:
                kwargs['auth']  = aiohttp.BasicAuth('api', self.internal_token)
            self.session = aiohttp.ClientSession(**kwargs)

    async def login(self):
        await self._ensure_session()
        self._ensure_has_credentials()
        await self._do_login()
        await self._maybe_impersonate()

    async def _do_login(self):
        if self.internal_token:
            # do something with aiohttp.ClientSession(headers={'Authorization': "Basic ..."})
            raise Exception("Sorry, I haven't implemented internal tokens in aioclient")
        payload = {
            'password'  : self.password,
            'username'  : self.username,
        }
        await self.post('users', '/sessions/', payload)

    async def _maybe_impersonate(self):
        if self.impersonate:
            raise Exception("Sorry, I haven't implemented impersonation yet")

    async def post(self, service, path, payload):
        url = self.url(service, path)
        with async_timeout.timeout(10):
            async with self.session.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}) as response:
                return await self._validate_response('POST', url, response)

    async def rawput(self, url, data, headers):
        async with self.session.put(url, data=data, headers=headers) as response:
            return await self._validate_response('PUT', url, response)

    async def rawget(self, url):
        await self._ensure_session()
        async with self.session.get(url) as response:
            return await self._validate_response('GET', url, response)

    async def _validate_response(self, method, url, response):
        text = await response.text()
        if not (response.status >= 200 and response.status < 300):
            raise diax.errors.RequestError(method, url, response)
        try:
            return json.loads(text), response.headers
        except ValueError:
            return text, response.headers

def create(args):
    "Create a client to talk to 3DIAX with the specified environment"
    return AsyncClient(
        certificate_bundle  = args.certificate_bundle,
        environment         = args.environment,
        impersonate         = args.impersonate,
        internal_token      = args.internal_token,
        password            = args.password,
        username            = args.username,
    )

