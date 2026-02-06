from app.models.tag import Tag

def test_tag_to_dict():
    new_tag = Tag(
        id=1,
        name="Electronics"
    )

    tag_dict = new_tag.to_dict()

    assert tag_dict['id'] == 1
    assert tag_dict['name'] == "Electronics"
    assert len(tag_dict) == 2 
