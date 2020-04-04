import abc
import cgi
import collections
import http.server
import json
import os
import re
import socketserver
import urllib.parse
from copy import deepcopy
from typing import (Any, Callable, Dict, List, Match, Pattern, Tuple, Type,
                    Union)

from .log import logger
from .utils import classproperty
from .errors import ApiError, InternalError, NotFound


class HeaderDict(dict):

    class Key(str):

        def __hash__(self) -> int:
            return hash(self.title())

        def __eq__(self, other) -> bool:
            return self.title() == other.title()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.update(*args, **kwargs)

    def __contains__(self, key) -> bool:
        key = self.Key(key)
        return super().__contains__(key)

    def __setitem__(self, key, value) -> Any:
        key = self.Key(key)
        super().__setitem__(key, value)

    def get(self, key, default=None) -> Any:
        key = self.Key(key)
        return super().get(key, default)

    __getitem__ = get

    def update(self, *args, **kwargs) -> None:
        d = dict(*args, **kwargs)
        for k, v in d.items():
            self[self.Key(k)] = v

Request = collections.namedtuple(
    'Request', 'address, method, path, query, parameters, headers, data')


class RequestHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    timeout = 15

    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

    def do_GET(self) -> None:
        self._dispatch('GET')

    def do_POST(self) -> None:
        self._dispatch('POST')

    def do_PATCH(self) -> None:
        self._dispatch('PATCH')

    def do_DELETE(self) -> None:
        self._dispatch('DELETE')

    def _parse_uri(self) -> Tuple[str, Dict[str, str]]:
        parsed = urllib.parse.urlsplit(self.path)
        return parsed.path, dict(urllib.parse.parse_qsl(parsed.query))

    def _respond(self, response) -> None:
        if isinstance(response, tuple):
            status_code, response = response
        else:
            status_code = 200
        if response is None:
            data = b''
        else:
            data = json.dumps(response, ensure_ascii=False,
                              indent=2).encode('u8')
        self.send_response(status_code)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': str(len(data))
        }
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)
        self.wfile.flush()

    def _dispatch(self, method: str) -> None:
        try:
            path, query = self._parse_uri()
            headers = HeaderDict(self.headers)
            content_length = int(headers.get('content-length', 0))
            data = None
            if content_length:
                content_type, pdict = cgi.parse_header(
                    headers.get('content-type', ''))
                if content_type != 'application/json':
                    raise ApiError
                content = self.rfile.read(content_length).decode(
                    pdict.get('charset', 'utf-8'))
                data = json.loads(content)
            match = None
            for endpoint in self.server.get_endpoints():
                match = endpoint.match(path)
                if match:
                    break
            if not match:
                raise NotFound
            request = Request(deepcopy(self.client_address), method,
                              path, query, match.groupdict(), headers, data)
            callback = getattr(endpoint(request), method.lower(), None)
            if not callable(callback):
                raise ApiError
            response = callback()
        except ApiError as e:
            response = e.get_response()
        except Exception as e:
            logger.exception(e)
            response = InternalError(e).get_response()
        self._respond(response)


class Endpoint(abc.ABC):
    path: str

    def __init__(self, request: Request) -> None:
        self.request = request

    @classproperty
    def regex(cls) -> Pattern[str]:  # pylint: disable=no-self-argument
        return re.compile(re.escape(cls.path).replace('<', '(?P<').replace('>', '>.*?)') + '$', re.I)

    @classmethod
    def match(cls, path) -> Match[str]:
        return cls.regex.match(path)  # pylint: disable=no-member


class ApiServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, host, port) -> None:
        super().__init__((host, port), RequestHandler)
        self._endpoints = set()

    def register_endpoint(self, endpoint: Type[Endpoint]) -> 'Server':
        self._endpoints.add(endpoint)
        return self

    def get_endpoints(self) -> Tuple[Type[Endpoint]]:
        return self._endpoints
