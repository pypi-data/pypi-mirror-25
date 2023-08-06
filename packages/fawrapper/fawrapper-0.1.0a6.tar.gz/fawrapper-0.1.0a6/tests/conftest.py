from os.path import join
import os
from pytest import fixture
from vcr import VCR
from fawrapper.requestmaker import RequestMaker
from fawrapper import FieldawareAPIClient

api_path = '/'
host = 'api.fieldaware.net'
api_key = os.environ['FIELDAWARE_TOKEN']

@fixture
def api():
    return FieldawareAPIClient()

@fixture
def request_maker():
    return RequestMaker(host, api_key)


@fixture
def vcr_cassette_path(request, vcr_cassette_name):
    # USED BY VCRPY
    # Put all cassettes in tests/api_returns/{module}/{test}.json
    return join('tests/api_returns', request.module.__name__, vcr_cassette_name)


@fixture
def vcr(request, vcr_config):
    # USED BY VCRPY
    """The VCR instance"""
    kwargs = dict(
        path_transformer=VCR.ensure_suffix(".json"),
        serializer='json',
        filter_headers= [('Authorization', 'DUMMY')],
        #record_mode='once',
        record_mode='new_episodes',
        #record_mode='none',
    )
    marker = request.node.get_marker('vcr')
    record_mode = request.config.getoption('--vcr-record-mode')

    kwargs.update(vcr_config)
    if marker:
        kwargs.update(marker.kwargs)
    if record_mode:
        kwargs['record_mode'] = record_mode

    vcr = VCR(**kwargs)
    return vcr

@fixture
def recorded():
    return vcr
