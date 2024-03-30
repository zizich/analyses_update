from sqlalchemy import Column, Integer, String

from db.base import Base


class Nurse(Base):
    __tablename__ = 'nurse'

    id = Column(Integer, primary_key=True)
    fio = Column(String)
    phone = Column(Integer)
    city = Column(String)

# todo таблица аттрибут заказа
# class NurseDateSelected(Base):
#     __tablename__ = 'nurse_date_selected'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(String)
#     nurse_id = Column(Integer)
#     user_id = Column(Integer)
#     emoji = Column(String)
#     city = Column(String)
#     delivery = Column(String)


# todo Должно рассчитываться на основе стоимости заказов и стоимоти работ Медсестры
# class NurseProfit(Base):
#     __tablename__ = 'nurse_profit'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(String)
#     nurse_id = Column(Integer)
#     name = Column(String)
#     analyses = Column(Enum)
#     price = Column(Integer)
#     prime_cost = Column(Integer)
#     income = Column(Integer)
#

# todo Аттрибут медсестры
# class NurseSalary(Base):
#     __tablename__ = 'nurse_salary'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     nurse_id = Column(Integer)
#     date = Column(String)
#     cash_day = Column(Integer)
#     cash_delivery = Column(Integer)
