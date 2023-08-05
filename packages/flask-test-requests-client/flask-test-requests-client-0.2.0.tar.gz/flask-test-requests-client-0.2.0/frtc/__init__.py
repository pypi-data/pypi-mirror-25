import json

import chardet

from requests.utils import get_encoding_from_headers


class TestClient(object):
    def __init__(self, client):
        self.client = client

    def get(self, url):
        return Response(self.client.get(url))


class Response(object):
    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def text(self):
        return self.response.get_data().decode(encoding=self.apparent_encoding)

    def json(self):
        return json.loads(self.text)

    @property
    def headers(self):
        return dict(self.response.headers.items(lower=False))

    @property
    def _headers(self):
        return dict(self.response.headers.items(lower=True))

    @property
    def apparent_encoding(self):
        return chardet.detect(self.response.get_data())['encoding']

    @property
    def encoding(self):
        if self._headers['content-type'] == "application/json":
            return None
        return get_encoding_from_headers(self.headers) or 'utf-8'
