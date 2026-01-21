from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..db import db

class ItemTag(db.Model):
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tag.id'), primary_key=True)