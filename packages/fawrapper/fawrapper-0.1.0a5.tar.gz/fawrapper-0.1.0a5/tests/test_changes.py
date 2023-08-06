"""Test changes endpoint on api"""
from fawrapper.utils import persist_token, read_token
from pytest import mark
from fawrapper.models import Change


def test_token_save_and_read_on_disk(tmpdir):
    token = '1234567'
    file = tmpdir.mkdir('fawrapper/').join('tmp_token_db')
    persist_token(token, file=file)
    assert read_token(file=file) == token


@mark.vcr
def test_get_token(api):
    token = api.changes.get_current_token()
    assert token == 259817214


@mark.vcr
def test_get_changes_since_token(api):
    changes = api.changes.list(since_token=259817200)
    for each in changes:
        assert isinstance(each, Change)




