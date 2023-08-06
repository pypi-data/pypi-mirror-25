"""Test the items resource on the api."""
from pytest import mark

from fawrapper import FieldawareAPIClient
from fawrapper.models import Item


@mark.vcr
def test_full_items_list():
    api = FieldawareAPIClient()
    items_list = api.items.list()
    item = next(items_list) # Only need to test first item
    assert isinstance(item, Item)
    assert item.name is not None
    assert item.part_number is not None



