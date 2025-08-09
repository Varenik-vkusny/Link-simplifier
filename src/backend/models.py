from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password_hash = Column(String, index=True)

    link = relationship('Link', back_populates='owner')


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, index=True)
    original_link = Column(String, index=True)
    short_code = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    click_count = Column(Integer, default=0, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='link')