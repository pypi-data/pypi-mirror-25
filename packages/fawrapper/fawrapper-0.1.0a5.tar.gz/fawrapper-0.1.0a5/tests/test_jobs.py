"""Test Jobs list from api"""
from pytest import mark, fixture, raises
from unittest import mock
from datetime import datetime
from unittest.mock import Mock

from fawrapper import FieldawareAPIClient
from fawrapper.utils import format_time_to_iso
from fawrapper.models import Jobs, Item
from fawrapper.exceptions import APIValidationError


@mark.vcr
def test_items_used_in_job(api):
    job_uuid = '427174cd4cd54f9e9cd35fe9a57b01c7'
    job = api.jobs.get(job_uuid)
    assert type(job.items_used) is list
    assert type(job.items_used[0]) is Item
    assert len(job.items_used) > 0
    assert job.items_used[0].name == 'Travel - Mileage'


@mark.vcr
def test_job_lead_change(api):
    job_uuid = 'aa0cf993283741ea97ec48924b17af60'
    job = api.jobs.get(job_uuid)

    filters = {'firstName': 'Johnny'}
    user = next(api.users.list(filters))
    assert user.first_name == 'Johnny'

    job.job_lead = user
    assert job.job_lead.first_name == 'Johnny'

    changed_job = api.jobs.get(job_uuid)
    assert changed_job.job_lead.first_name == 'Johnny'


@mark.vcr
def test_job_list_filters_completed(api):
    filters = {'state': 'completed'}
    job = next(api.jobs.list(filters))
    assert job.state == 'completed'


@mark.vcr
def test_job_list_filters_scheduled(api):
    filters = {'state': 'scheduled'}
    job = next(api.jobs.list(filters))
    assert job.state == 'scheduled'

@mark.vcr
def test_get_all_jobs(api):
    start = format_time_to_iso(2017, 1, 1)
    end = format_time_to_iso(2017, 9, 30)
    filters = {'start': start, 'end': end}
    job = next(api.jobs.list(filters))
    assert job.uuid is not None
    assert job.description is not None
    assert job.location is not None
    assert job.job_lead is not None

@mark.vcr
def test_get_all_jobs_no_filters(api):
    job = next(api.jobs.list())
    assert job.uuid is not None


def test_validate_empty_filters():
    with mock.patch('fawrapper.models.models.format_time_to_iso',
                    return_value='test_string'):
        returned_filters = Jobs()._validate_filters()
    assert type(returned_filters) is dict
    assert type(returned_filters['start']) is str
    assert returned_filters['start'] == 'test_string'


def test_validate_default_end_filter():
    with mock.patch('fawrapper.models.models.format_time_to_iso',
                    return_value='test_string'):
        returned_filters = Jobs()._validate_filters()
    assert type(returned_filters['end']) is str
    assert returned_filters['end'] == 'test_string'


def test_incorrect_filters_type():
    with raises(TypeError):
        Jobs()._validate_filters(filters=list('some_value'))


def test_invalid_filter_raises():
    invalid_filters = {'invalid_key': 'invalid_value'}
    with raises(Exception):
        Jobs()._validate_filters(invalid_filters)











