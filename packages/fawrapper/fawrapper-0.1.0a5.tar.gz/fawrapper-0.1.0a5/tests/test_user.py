"""Test user instances"""
from pytest import mark

from fawrapper.models import User


@mark.vcr
def test_pull_details(request_maker):
    real_uuid = "fd55615331be40bcb2758e9e585cff54"
    user = User(request_maker, uuid=real_uuid)
    assert user.first_name is None
    assert user.archived is None
    assert user.role is None
    assert user.last_name is None
    user.pull_details()
    assert user.archived is False
    assert user.role == 'Admin'
    assert user.last_name == 'Martinez'
    assert user.first_name == 'Chase'

