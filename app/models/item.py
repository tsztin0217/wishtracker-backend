from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime, timezone

class Item(db.Model):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[float]
    img_url: Mapped[str]
    website_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped['User'] = relationship(back_populates='items')
    tags: Mapped[list['Tag']] = relationship(secondary='item_tag', back_populates='items')