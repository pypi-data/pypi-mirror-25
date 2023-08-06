import json


class MockResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text or 'default_text'
        self.url = 'mock_url'

    def json(self):
        return json.loads(self.text)

    def text(self):
        return self.text


def read_file(path):
    with open(path) as f:
        return f.read()
