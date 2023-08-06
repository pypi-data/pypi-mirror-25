from urllib.parse import urlencode
import json

import requests

from fawrapper.exceptions import (
    APIValidationError, AuthenticationError,
    BadRequest, ConflictError, NotFoundError, UnknownStatusCode)


def build_url(hostname, path, params=None, protocol='https://'):
    url =  f'{protocol}{hostname}{path}'
    if params:
        url += '?' + urlencode(params)
    return url
        

class RequestMaker:
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key

        self.headers = {"Authorization": f"Token {self.api_key}",
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Host": self.host}

    def _request(self, method, path, data=None, params=None):
        url = build_url(self.host, path, params)
        #import pdb; pdb.set_trace()
        response = requests.request(
            headers=self.headers,
            method=method,
            url=url,
            data=data or {},
        )
        self._check_status_code(response)
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text

    def get(self, uri, params=None):
        """Retrieve an object(s) from api"""
        return self._request('get', uri, params=params)

    def post(self, uri, data=None):
        """Create a new object"""
        if type(data) is dict:
            data = json.dumps(data)
            self._request('post', uri, data)

    def put(self, uri, data=None):
        """Update an existing object"""
        self._request('put', uri, data)

    def delete(self, uri):
        """Delete an existing object"""
        self._request('delete', uri)

    def _check_status_code(self, response):
        error_codes = {
            422: APIValidationError,
            401: AuthenticationError,
            400: BadRequest,
            409: ConflictError,
            404: NotFoundError,
        }
        if response.status_code in error_codes:
            raise error_codes[response.status_code](
                response.text , response.url)

        success_codes = {
            200: 'OK',
            204: 'No Content',
            201: '?',
        }
        if response.status_code not in success_codes:
            raise UnknownStatusCode(
                f'{response.status_code}: {response.text}, {response.url}')
