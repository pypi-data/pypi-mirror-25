"""Test changes endpoint on api"""
from fawrapper.utils import persist_token, read_token


def test_token_save_and_read_on_disk(tmpdir):
    token = '1234567'
    file = tmpdir.mkdir('fawrapper/').join('tmp_token_db')
    persist_token(token, file=file)
    assert read_token(file=file) == token


def test_get_token(api):
    api.changes.list()


