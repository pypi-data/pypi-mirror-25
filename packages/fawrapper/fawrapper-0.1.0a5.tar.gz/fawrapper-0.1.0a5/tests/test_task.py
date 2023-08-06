"""Test the Task object on the api"""

from fawrapper.models import TaskInJob, Task, ItemInTask, Item
from pytest import mark


@mark.vcr
def test_task_in_job_init(request_maker):
    job_uuid = '427174cd4cd54f9e9cd35fe9a57b01c7'
    task_uuid = '116efd341c1f4e42a3e3544c10c1c3ad'
    params = {'uuid': task_uuid, 'job_uuid': job_uuid}
    task = TaskInJob(requester=request_maker, **params)
    task.pull_details()
    assert task.uuid == task_uuid
    assert task.job_uuid == job_uuid
    assert task.attachments is not None
    assert task.unit_price == 0.0
    assert task.unit_cost == 0.0
    assert type(task.note) is str


@mark.vcr
def test_task_in_taskinjob_init(request_maker):
    job_uuid = '427174cd4cd54f9e9cd35fe9a57b01c7'
    task_uuid = '116efd341c1f4e42a3e3544c10c1c3ad'
    params = {'uuid': task_uuid, 'job_uuid': job_uuid}
    task = TaskInJob(requester=request_maker, **params)
    task.pull_details()
    assert type(task.task) is Task
    assert task.task.uuid == 'b99787ec09dd4c0ba84e26c41749c570'
    assert task.task.taxable == False
    assert task.task.name == 'Service and Repair'


@mark.vcr
def test_items_in_task_in_job(request_maker):
    job_uuid = '427174cd4cd54f9e9cd35fe9a57b01c7'
    task_uuid = '116efd341c1f4e42a3e3544c10c1c3ad'
    params = {'uuid': task_uuid, 'job_uuid': job_uuid}
    task_in_job = TaskInJob(requester=request_maker, **params)
    task_in_job.pull_details()
    assert type(task_in_job.items) is list
    assert len(task_in_job.items) > 0
    for each in task_in_job.items:
        assert isinstance(each, ItemInTask)
        assert each._item is not None
        assert each.uuid is not None

        # Defaults
        assert isinstance(each.item, Item)
        assert each.item.uuid is not None
        assert each.item.name is not None
        assert each.item.description is not None

        # Pulled from api
        assert each.item.part_number is not None
        assert type(each.item.unit_cost) is float
        assert type(each.item.unit_price) is float





