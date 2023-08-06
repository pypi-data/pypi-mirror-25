from random import choice
import json
from urllib.parse import parse_qs

from swagger_parser import SwaggerParser
from decouple import config
from flask import Flask, jsonify, g, request, current_app
from flask_cors import CORS
from swagger_parser import SwaggerParser
from werkzeug.local import LocalProxy


def get_swagger_parser():
    parser = getattr(g, "_swagger_parser", None)
    if parser is None:
        parser = g._swagger_parser = SwaggerParser(swagger_path=current_app.config["SWAGGER_PATH"],
                                                   use_example=True)
    return parser


app = Flask(__name__)
cors = CORS(app)
parser = LocalProxy(get_swagger_parser)


@app.route("/<path:path>")
def root(path):
    params = request.data.decode("utf-8")
    query = parse_qs(request.query_string)
    path = "/{}".format(path)
    method = request.method.lower()
    response = parser.get_request_data(path,
                                       method,
                                       body=params)

    status, body = choice(list(response.items()))
    body = body or None
    return (jsonify(body), status)


# valid = parser.validate_request(path,
#                                 method,
#                                 body=params,
#                                 query=query)
#
# body["valid"] = valid
