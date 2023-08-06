import json

import yaml
import requests


def load_file(path):
    try:
        response = requests.get(path)
        return response.content.decode("utf-8")
    except:
        with open(path, "r") as f:
            return f.read()


def parse_body(body):
    try:
        return yaml.load(body)
    except:
        return json.load(body)


def load_dict_from_path(path):
    return parse_body(load_file(path))
