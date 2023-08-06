from swagger_parser import SwaggerParser

from .utils import load_dict_from_path


class MockResponseConfig(object):

    def __init__(self, swagger_path, validate_request=False):
        self.swagger_path = swagger_path
        self.validate_request = validate_request

    @property
    def swagger_parser(self):
        swagger_dict = load_dict_from_path(self.swagger_path)
        return SwaggerParser(swagger_dict=swagger_dict)
