from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    items: Mapped[list['Item']] = relationship(secondary='item_tag', back_populates='tags')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='owned_tags')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
