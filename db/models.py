from sqlalchemy import Column, Integer, String, Enum, BLOB

from db.base import Base


class Analyses(Base):
    __tablename__ = 'analyses'

    sequence_number = Column(Integer, primary_key=True, autoincrement=True)
    code_number = Column(String)
    name = Column(String)
    synonyms = Column(String)
    info = Column(String)
    tube = Column(String)
    readiness = Column(Integer)
    sale = Column(Integer)
    price = Column(Integer)
    prime_cost = Column(Integer)
    stop = Column(Integer)
    complex = Column(String)


class AnalysesComplex(Base):
    __tablename__ = 'analyses_complex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_complex = Column(String)
    code_complex = Column(Integer)
    code_analyses = Column(String)


class CitiesPayment(Base):
    __tablename__ = 'cities_payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    sampling = Column(Integer)
    _exit = Column(name='exit')
    address = Column(String)
    phone = Column(String)
    bank = Column(String)
    all_sale = Column(String)
    nurse_delivery = Column(Integer)
    nurse_income_day = Column(Integer)


class Nurse(Base):
    __tablename__ = 'nurse'

    nurse_id = Column(Integer)
    fio = Column(String)
    phone = Column(Integer)
    city = Column(String)


class NurseDateSelected(Base):
    __tablename__ = 'nurse_date_selected'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    nurse_id = Column(Integer)
    user_id = Column(Integer)
    emoji = Column(String)
    city = Column(String)
    delivery = Column(String)


class NurseOrders(Base):
    __tablename__ = 'nurse_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    nurse_id = Column(Integer)
    users_id = Column(Integer)
    name = Column(String)
    analyses = Column(String)
    tube = Column(String)
    city = Column(String)
    delivery = Column(String)
    address = Column(String)
    comment = Column(String)
    done = Column(String)
    confirm = Column(String)
    price = Column(Integer)
    price_cost = Column(Integer)
    income = Column(Integer)


class NurseProfit(Base):
    __tablename__ = 'nurse_profit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    nurse_id = Column(Integer)
    name = Column(String)
    analyses = Column(Enum)
    price = Column(Integer)
    prime_cost = Column(Integer)
    income = Column(Integer)


class NurseSalary(Base):
    __tablename__ = 'nurse_salary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nurse_id = Column(String)
    date = Column(String)
    cash_day = Column(Integer)
    cash_delivery = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    fio = Column(String)
    birth_date = Column(String)
    phone = Column(Integer)
    email = Column(String)
    city = Column(String)
    address = Column(String)
    subscribe = Column(String)
    info = Column(String)
    others = Column(String)
    photo = Column(BLOB)
    reference = Column(String)


class UsersAnalysesSelected(Base):
    __tablename__ = 'users_analyses_selected'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code_analyses = Column(Integer)
    name_analyses = Column(String)
    tube = Column(String)
    readiness = Column(String)
    price = Column(String)
    price_cost = Column(String)
    income = Column(String)
    user_id = Column(String)


class UsersArchive(Base):
    __tablename__ = 'users_archive'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    user_id = Column(String)
    nurse_id = Column(String)
    name = Column(String)
    analysis = Column(String)
    price = Column(Integer)
    address = Column(String)
    city = Column(String)
    delivery = Column(String)
    comment = Column(String)
    confirm = Column(String)


class UsersComments(Base):
    __tablename__ = 'users_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    comment = Column(String)


class UsersOrders(Base):
    __tablename__ = 'users_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    user_id = Column(String)
    nurse_id = Column(String)
    name = Column(String)
    analysis = Column(String)
    price = Column(Integer)
    address = Column(String)
    city = Column(String)
    delivery = Column(String)
    comment = Column(String)
    confirm = Column(String)


class UsersPattern(Base):
    __tablename__ = 'users_pattern'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    name_pattern = Column(String)
    analyses_sequence_numbers = Column(String)


class UsersSelected(Base):
    __tablename__ = 'users_selected'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    fio = Column(String)
    birth_date = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
