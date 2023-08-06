from unittest.mock import patch
import json

import pytest

from fawrapper.exceptions import (
    APIValidationError, AuthenticationError,
    BadRequest, ConflictError, NotFoundError, UnknownStatusCode)
from fawrapper.requestmaker import build_url
from tests.conftest import api_key, host
from .tools import MockResponse


def test_minimum_init(request_maker):
    assert request_maker.host == host
    assert request_maker.api_key == api_key

    assert request_maker.headers == {
        'Authorization': f'Token {api_key}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Host': request_maker.host,
    }


def test_build_url():
    url = build_url(protocol='https://', hostname='api.net', path='/')
    assert url == 'https://api.net/'

    url = build_url('api.net', '/path/')
    assert url == 'https://api.net/path/'

    url = build_url('api.net', '/path/', params={'key': 'value'})
    assert url == 'https://api.net/path/?key=value'


@patch('fawrapper.requestmaker.requests.request')
def test_requests_get_is_called(requests_request, request_maker):
    requests_request.return_value = MockResponse(200, "test")
    request_maker.get('/something')
    requests_request.assert_called_with(
        method='get',
        url=f'https://{host}/something',
        data={},
        headers=request_maker.headers,
    )


@patch('fawrapper.requestmaker.requests.request')
def test_requests_get_is_called_with_params(requests_request, request_maker):
    requests_request.return_value = MockResponse(200, '""')
    params = {'key': 'value'}
    request_maker.get('/something/', params)
    requests_request.assert_called_with(
        method='get',
        url=f'https://{host}/something/?key=value',
        data={},
        headers=request_maker.headers,
    )


@patch('fawrapper.requestmaker.requests.request')
def test_requests_post_is_called(requests_request, request_maker):
    requests_request.return_value = MockResponse(200, '""')
    request_maker.post('/something/', {'key': 'value'})
    requests_request.assert_called_with(
        method='post',
        url=f'https://{request_maker.host}/something/',
        data=json.dumps({"key": "value"}),
        headers=request_maker.headers,
    )


@patch('fawrapper.requestmaker.requests.request')
def test_requests_put_is_called(requests_request, request_maker):
    requests_request.return_value = MockResponse(200, '""')
    request_maker.put('/something/', {'key': 'value'})
    requests_request.assert_called_with(
        method='put',
        url=f'https://{request_maker.host}/something/',
        data={"key": "value"},
        headers=request_maker.headers,
    )


@patch('fawrapper.requestmaker.requests.request')
def test_requests_delete_is_called(requests_request, request_maker):
    requests_request.return_value = MockResponse(200, '""')
    request_maker.delete('/something/')
    requests_request.assert_called_with(
        method='delete',
        url=f'https://{request_maker.host}/something/',
        data={},
        headers=request_maker.headers,
    )


@pytest.mark.parametrize('status_code,exception', [
    (422, APIValidationError),
    (409, ConflictError),
    (401, AuthenticationError),
    (404, NotFoundError),
    (400, BadRequest)])
def test_error_status_codes(status_code, exception, request_maker):
    with pytest.raises(exception) as error:
        response = MockResponse(status_code, 'error message')
        request_maker._check_status_code(response)
    assert error.value.args[0] == 'error message'


@pytest.mark.parametrize('status_code', [200, 201, 204])
def test_200_status_code_passes(status_code, request_maker):
    response = MockResponse(status_code, '""')
    request_maker._check_status_code(response)


def test_unknown_status_code_raises_exception(request_maker):
    with pytest.raises(UnknownStatusCode) as error:
        response = MockResponse(888, 'unknown error message')
        request_maker._check_status_code(response)
    assert error.value.args[0] == '888: unknown error message, mock_url'


