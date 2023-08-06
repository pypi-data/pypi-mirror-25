from urllib.parse import parse_qs


class RequestParser(object):

    def __init__(self, request, path):
        self.body = request.data.decode("utf-8")
        self.query = parse_qs(request.query_string)
        self.path = "/{}".format(path)
        self.method = request.method.lower()
