from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    oauth_provider: Mapped[str] = mapped_column(default='Google')
    oauth_id: Mapped[str]
    email: Mapped[str]
    name: Mapped[str]
    items: Mapped[list['Item']] = relationship(back_populates='user')

    @staticmethod
    def get_or_create(oauth_provider, oauth_id, email, name=None):
        user = User.query.filter_by(
            oauth_provider = oauth_provider,
            oauth_id = oauth_id
        ).first()

        if user:
            user.name = name
        else:
            user = User(
                oauth_provider = oauth_provider,
                oauth_id = oauth_id,
                email = email,
                name = name
            )
            db.session.add(user)

        db.session.commit()
        return user
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'oauth_provider': self.oauth_provider,
            'oauth_id': self.oauth_id
        }