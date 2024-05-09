from sqlalchemy import Column, BigInteger, Integer, String

from db.base import OrmModel


class User(OrmModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String)
    address = Column(String)
