from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .item_tag import item_tag

class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    items: Mapped[list['Item']] = relationship(secondary=item_tag, back_populates='tags')
