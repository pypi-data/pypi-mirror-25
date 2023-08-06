from random import choice

from .config import MockResponseConfig
from .parser import RequestParser


class ResponseFetcher(object):

    def __init__(self, config, request, path):
        self.config = config
        self.request = request
        self.path = path

    @property
    def swagger_parser(self):
        return self.config.swagger_parser

    @property
    def request_parser(self):
        return RequestParser(self.request, self.path)

    @property
    def response(self):
        return self.swagger_parser.get_request_data(self.request_parser.path,
                                                    self.request_parser.method,
                                                    body=self.request_parser.body)

    def fetch(self):
        status, body = choice(list(self.response.items()))
        return int(status), body


class MockResponseBuilder(object):

    def __init__(self, swagger_path, validate_request=False):
        self.config = MockResponseConfig(swagger_path, validate_request)

    def build(self, request, path):
        return ResponseFetcher(self.config, request, path).fetch()
