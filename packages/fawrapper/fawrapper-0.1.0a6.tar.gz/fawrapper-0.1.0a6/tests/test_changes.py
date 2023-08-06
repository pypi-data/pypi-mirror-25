"""Test changes endpoint on api"""
from fawrapper.utils import persist_token, read_token
from pytest import mark
from fawrapper.models import Change
from unittest.mock import patch


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


@patch('fawrapper.models.models.persist_token') # Don't create a file
@mark.vcr
def test_get_changes_no_token_provided_no_file(persist_token, api):
    changes = api.changes.list()
    assert len(list(changes)) == 0


@patch('fawrapper.models.models.persist_token') # Don't create a file
@patch('fawrapper.models.models.read_token')
@mark.vcr
def test_get_changes_no_token_provided(read_token, persist_token, api):
    read_token.return_value = 25981700
    changes = api.changes.list()
    assert isinstance(next(changes), Change)


