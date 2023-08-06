"""Test Job objects on the api"""
from pytest import mark
from fawrapper.models import Jobs, User, TaskInJob
from fawrapper import FieldawareAPIClient


@mark.vcr
def test_job_lead_attribute_is_user_instance():
    api = FieldawareAPIClient()
    job = api.jobs.get('7b6c125c296449ed9bf4763aaf0dbaa0')
    assert isinstance(job.job_lead, User)
    assert job.job_lead.uuid == 'a2a028db0a064ef0b95d57becd7c1e0c'
    assert job.job_lead.first_name == 'Office'


@mark.vcr
def test_tasks_attribute_is_list_of_instances():
    api = FieldawareAPIClient()
    job = api.jobs.get('7b6c125c296449ed9bf4763aaf0dbaa0')
    assert isinstance(job.tasks, list)
    for each in job.tasks:
        assert isinstance(each, TaskInJob)

