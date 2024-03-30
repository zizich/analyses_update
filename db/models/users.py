from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fio = Column(String)
    birth_date = Column(Date)  # На сколько важно это поле?
    phone = Column(Integer)
    email = Column(String, nullable=True)
    city = Column(String)
    address = Column(String, nullable=True)

    orders = relationship('Order', back_populates='user')

    # todo Не ясно назначение
    # subscribe = Column(String)
    # info = Column(String)
    # others = Column(String)
    # reference = Column(String)
    # photo = Column(BLOB)


# class UsersAnalysesSelected(Base):
#     __tablename__ = 'users_analyses_selected'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     code_analyses = Column(Integer)
#     name_analyses = Column(String)
#     tube = Column(String)
#     readiness = Column(String)
#     price = Column(String)
#     price_cost = Column(String)
#     income = Column(String)
#     user_id = Column(String)


# class UsersArchive(Base):
#     __tablename__ = 'users_archive'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(String)
#     user_id = Column(String)
#     nurse_id = Column(String)
#     name = Column(String)
#     analysis = Column(String)
#     price = Column(Integer)
#     address = Column(String)
#     city = Column(String)
#     delivery = Column(String)
#     comment = Column(String)
#     confirm = Column(String)

# todo Аттрибут заказа
# class UsersComments(Base):
#     __tablename__ = 'users_comments'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(String)
#     comment = Column(String)


# class UsersOrders(Base):
#     __tablename__ = 'users_orders'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(String)
#     user_id = Column(String)
#     nurse_id = Column(String)
#     name = Column(String)
#     analysis = Column(String)
#     price = Column(Integer)
#     address = Column(String)
#     city = Column(String)
#     delivery = Column(String)
#     comment = Column(String)
#     confirm = Column(String)


# todo Черновик заказа
# class UsersPattern(Base):
#     __tablename__ = 'users_pattern'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(String)
#     name_pattern = Column(String)
#     analyses_sequence_numbers = Column(String)


# class UsersSelected(Base):
#     __tablename__ = 'users_selected'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(String)
#     fio = Column(String)
#     birth_date = Column(String)
#     phone = Column(String)
#     email = Column(String)
#     address = Column(String)
#     city = Column(String)
