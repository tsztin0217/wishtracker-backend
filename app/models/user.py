from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    oauth_provider: Mapped[str] = mapped_column(default="Google")
    oauth_id: Mapped[str]
    items: Mapped[list["Item"]] = relationship(back_populates="user")


