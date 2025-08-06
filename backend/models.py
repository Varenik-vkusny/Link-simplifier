from sqlalchemy import String, Integer, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
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
    short_link = Column(String, unique=True , index=True)
    created_at = Column(DateTime, default=datetime.now(tz='Asia/Almaty'))
    owner_id = Column(Integer, ForeignKey='users.id', index=True)

    owner = relationship('User', back_populates='link')