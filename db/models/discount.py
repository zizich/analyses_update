from _decimal import Decimal
from datetime import date

from sqlalchemy import Column, Integer, Date, DECIMAL, Enum

from db.base import Base
from db.utils import IsActiveStatus


class Discount(Base):
    __tablename__ = 'discount'

    id = Column(Integer, primary_key=True)
    created = Column(Date, default=date.today())
    discount = Column(DECIMAL, default=Decimal())
    status = Column(Enum(IsActiveStatus), default=IsActiveStatus.ACTIVE)
