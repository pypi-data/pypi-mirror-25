from decouple import config
from flask import Flask, g, request, current_app
from flask_cors import CORS
from werkzeug.local import LocalProxy

from swagger_stub_api.mock.response import MockResponseBuilder
from swagger_stub_api.renderers import render_response


def get_mock_response_builder():
    mock_response_builder = getattr(g, "_mock_response_builder", None)
    if mock_response_builder is None:
        mock_response_builder = MockResponseBuilder(current_app.config["SWAGGER_PATH"])
    return mock_response_builder


app = Flask(__name__)
cors = CORS(app)
mock_response_builder = LocalProxy(get_mock_response_builder)


@app.route("/<path:path>")
def root(path):
    status, body = mock_response_builder.build(request, path)
    return render_response(body, status)
