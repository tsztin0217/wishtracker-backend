from app.models.item import Item
from app.db import db
import pytest

def test_item_to_dict():
    new_item = Item(
        id = 1,
        name = "Test Item",
        description = "This is a test item",
        price = 19.99,
        img_url = "http://example.com/image.jpg",
        website_url = "http://example.com"
    )

    item_dict = new_item.to_dict()

    assert item_dict['id'] == 1
    assert item_dict['name'] == "Test Item"
    assert item_dict['description'] == "This is a test item"
    assert item_dict['price'] == 19.99
    assert item_dict['img_url'] == "http://example.com/image.jpg"
    assert item_dict['website_url'] == "http://example.com"