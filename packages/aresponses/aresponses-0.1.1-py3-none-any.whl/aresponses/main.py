import logging

import pytest
from aiohttp import web
from aiohttp.client_reqrep import ClientRequest
from aiohttp.connector import TCPConnector
from aiohttp.helpers import sentinel
from aiohttp.test_utils import BaseTestServer
from aiohttp.web_server import Server

from aresponses.utils import _text_matches_pattern, ANY

logger = logging.getLogger(__name__)


class ResponsesMockServer(BaseTestServer):
    ANY = ANY
    Response = web.Response

    def __init__(self, *, scheme=sentinel, host='127.0.0.1', **kwargs):
        self._responses = []
        self._host_patterns = set()
        self._exception = None
        super().__init__(scheme=scheme, host=host, **kwargs)

    async def _make_factory(self, debug=True, **kwargs):
        self.handler = Server(self._handler, loop=self._loop, debug=True, **kwargs)
        return self.handler

    async def _close_hook(self):
        return

    async def _handler(self, request):
        return self._find_response(request)

    def add(self, host_pattern, path_pattern, method_pattern, response):
        if isinstance(host_pattern, str):
            host_pattern = host_pattern.lower()

        if isinstance(method_pattern, str):
            method_pattern = method_pattern.lower()

        self._host_patterns.add(host_pattern)
        self._responses.append((host_pattern, path_pattern, method_pattern, response))

    def _host_matches(self, match_host):
        match_host = match_host.lower()
        for host_pattern in self._host_patterns:
            if _text_matches_pattern(host_pattern, match_host):
                return True

        return False

    def _find_response(self, request):
        host, path, method = request.host, request.path, request.method
        logger.info(f'Looking for match for {host} {path} {method}')
        i = 0
        for host_pattern, path_pattern, method_pattern, response in self._responses:
            if _text_matches_pattern(host_pattern, host):
                if _text_matches_pattern(path_pattern, path):
                    if _text_matches_pattern(method_pattern, method.lower()):
                        del self._responses[i]
                        if callable(response):
                            return response(request)
                        elif isinstance(response, str):
                            return web.Response(body=response)
                        return response
            i += 1
        self._exception = Exception(f"No Match found for {host} {path} {method}")
        # pytest.fail(str(self._exception))
        self._loop.stop()
        raise self._exception  # noqa

    async def __aenter__(self):
        await self.start_server(loop=self._loop)

        self._old_resolver_mock = TCPConnector._resolve_host

        async def _resolver_mock(_self, host, port):
            return [{
                'hostname': host, 'host': '127.0.0.1', 'port': self.port,
                'family': _self._family, 'proto': 0, 'flags': 0
            }]

        TCPConnector._resolve_host = _resolver_mock

        self._old_update_host = ClientRequest.update_host

        def new_update_host(_self, *args, **kwargs):
            val = self._old_update_host(_self, *args, **kwargs)
            _self.ssl = False
            return val

        ClientRequest.update_host = new_update_host
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        TCPConnector._resolve_host = self._old_resolver_mock
        ClientRequest.update_host = self._old_update_host

        await self.close()
        if self._exception:
            pytest.fail(str(self._exception))
            raise self._exception  # noqa


@pytest.yield_fixture
async def aresponses(event_loop):
    async with ResponsesMockServer(loop=event_loop) as server:
        yield server
