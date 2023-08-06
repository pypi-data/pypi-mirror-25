"""Test the Tasks object on the api"""
from pytest import mark

@mark.vcr
def test_tasks_list(api):
    task = next(api.tasks.list())
    assert task.uuid == '0382b04b53e340feb3c054bad29d646f'
    assert task.gl_account is None
    assert task.name == 'Prover'
    assert task.markup_type == 'fixed'
    assert task.taxable == True
    assert task.markup_value == 0.0
    assert task.custom_fields == {}
    assert task.est_duration == None
    assert task.unit_price == 0.0
    assert task.unit_cost == 0.0
    assert task.description == 'Needed for calibration'

