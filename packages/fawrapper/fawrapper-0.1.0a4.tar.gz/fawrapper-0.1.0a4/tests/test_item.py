"""Test the item object on the api."""
from pytest import mark
from fawrapper import FieldawareAPIClient
from fawrapper.models import Item, ItemInTask

@mark.vcr
def test_get_item_with_uuid():
    api = FieldawareAPIClient()
    item = api.items.get('0121fca8d1314f4093f911e35d427581')
    assert isinstance(item, Item)
    assert item.name is not None
    assert item.part_number is not None


def test_item_in_task_in_job_init(request_maker):
        job_uuid = '427174cd4cd54f9e9cd35fe9a57b01c7'
        task_in_job_uuid = '116efd341c1f4e42a3e3544c10c1c3ad'
        params = {'task_in_job_uuid': task_in_job_uuid, 'job_uuid': job_uuid}
        item = ItemInTask(requester=request_maker, **params)

