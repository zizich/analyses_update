from sqlalchemy import Column, Integer, String

from db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(Integer, unique=True, index=True, nullable=False)
    full_name = Column(String)
    address = Column(String)
