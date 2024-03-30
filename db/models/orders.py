from decimal import Decimal
from datetime import datetime
import enum

from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship

from db.base import Base


class OrderType(enum.Enum):
    HOME_VISIT = 0
    IN_CLINIC = 1


class OrderStatus(enum.Enum):
    NEW = 0
    CONFIRM = 1
    DONE = 2


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())
    users_id = Column(Integer, ForeignKey('User.id'))
    nurse_id = Column(Integer, ForeignKey('Nurse.id'), nullable=True)
    date = Column(Date, nullable=True)  # Дата, когда заказ был / будет выполнен
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    type = Column(Enum(OrderType), default=OrderType.HOME_VISIT)  # delivery
    price = Column(DECIMAL, default=Decimal(), nullable=True)
    address = Column(String, nullable=True)
    comment = Column(String, nullable=True)

    analyses = relationship('Analyse', back_populates='orders')
    user = relationship('User', back_populates='orders')

    # date = Column(String)
    # name = Column(String)  # Данные о клиенте
    # analyses = Column(String)
    # tube = Column(String)
    # city = Column(String)
    # done = Column(String)
    # confirm = Column(String)
    # price_cost = Column(Integer)
    # income = Column(Integer)
