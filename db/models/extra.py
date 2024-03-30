from sqlalchemy import Column, Integer, String

from db.base import Base


class CitiesPayment(Base):
    __tablename__ = 'cities_payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    address = Column(String)
    phone = Column(String)
    bank = Column(String)
    all_sale = Column(String)
    # sampling = Column(Integer)
    # nurse_delivery = Column(Integer)
    # nurse_income_day = Column(Integer)
    # _exit = Column(name='exit')


