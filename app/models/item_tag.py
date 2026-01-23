from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..db import db

class ItemTag(db.Model):
    __tablename__ = 'item_tag'
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)