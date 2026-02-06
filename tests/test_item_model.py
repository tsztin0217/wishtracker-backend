from app.models.item import Item
import pytest

def test_item_to_dict_with_all_fields():
    new_item = Item(
        id=1,
        name="Gaming Laptop",
        description="High performance gaming laptop",
        price=1299.99,
        img_url="http://example.com/laptop.jpg",
        website_url="http://example.com/product/laptop"
    )

    item_dict = new_item.to_dict()

    assert item_dict['id'] == 1
    assert item_dict['name'] == "Gaming Laptop"
    assert item_dict['description'] == "High performance gaming laptop"
    assert item_dict['price'] == 1299.99
    assert item_dict['img_url'] == "http://example.com/laptop.jpg"
    assert item_dict['website_url'] == "http://example.com/product/laptop"


def test_item_to_dict_with_minimal_fields():
    new_item = Item(
        id=2,
        name="Simple Item"
    )

    item_dict = new_item.to_dict()

    assert item_dict['id'] == 2
    assert item_dict['name'] == "Simple Item"
    assert item_dict.get('description') is None
    assert item_dict.get('price') is None


def test_item_to_dict_with_zero_price():
    new_item = Item(
        id=3,
        name="Free Item",
        price=0.0
    )

    item_dict = new_item.to_dict()

    assert item_dict['price'] == 0.0
    assert item_dict['name'] == "Free Item"


def test_item_to_dict_with_special_characters():
    new_item = Item(
        id=4,
        name="Item with 'quotes' & symbols",
        description="Description with émojis 🎮"
    )

    item_dict = new_item.to_dict()

    assert item_dict['name'] == "Item with 'quotes' & symbols"
    assert "émojis 🎮" in item_dict['description']
