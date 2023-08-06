from flask import Response, jsonify


def render_response(contents, status):
    if contents:
        return jsonify(contents), status
    return "", status
