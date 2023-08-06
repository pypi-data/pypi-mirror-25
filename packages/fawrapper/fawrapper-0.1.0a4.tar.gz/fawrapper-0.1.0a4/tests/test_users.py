from pytest import mark

from fawrapper import FieldawareAPIClient


@mark.vcr
def test_basic_users_list():
    api = FieldawareAPIClient()
    users = [user for user in api.users.list()]
    for user in users:
        assert hasattr(user, 'uuid')
        assert hasattr(user, 'email')
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')


@mark.vcr
def test_users_list_with_filters():
    api = FieldawareAPIClient()
    filters = {'firstName': 'faadmin'}
    users = api.users.list(filters)
    for each in users:
        assert each.first_name == 'faadmin'


@mark.vcr
def test_get_user_with_uuid():
    api = FieldawareAPIClient()
    uuid = '145a5454958d45c0956f0e36126363ac'
    user = api.users.get(uuid)
    assert user.email == 'faadmin@aphelpspetroleum.com'


def test_user_parse_from_dict():
    data = {
        'uuid': 'user_uuid',
        'email': 'user@email.com',
        'firstName': 'user_name'
    }
    api = FieldawareAPIClient('some_key')
    user = api.users._parse_to_instance(data)
    assert user.uuid == 'user_uuid'
    assert user.email == 'user@email.com'
    assert user.first_name == 'user_name'






