import enum
from decimal import Decimal

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import Mapped, relationship

from db.base import Base
from db.utils import IsActiveStatus


class AnalysesComplex(Base):
    __tablename__ = 'analyses_complex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    analyse_id = Column(Integer, ForeignKey('analyse.id'))
    complex_id = Column(Integer, ForeignKey('complex.id'))


class TubeType(enum.Enum):
    """Пробирка на которую надо брать анализ."""
    yellow = 0
    blue = 1
    purple = 2


class Analyse(Base):
    __tablename__ = 'analyse'

    id = Column(Integer, primary_key=True)  # sequence_number
    code_number = Column(String)
    name = Column(String)
    info = Column(String)
    tube = Column(Enum(TubeType))
    readiness_days = Column(Integer)
    status = Column(Enum(IsActiveStatus), default=IsActiveStatus.ACTIVE)  # stop

    price = Column(DECIMAL, default=Decimal())
    prime_cost = Column(DECIMAL, default=Decimal())

    complexes: Mapped[list['Complex']] = relationship(secondary=AnalysesComplex, back_populates="analyses")
    orders = relationship('Order', back_populates='analyses')


class Complex(Base):
    __tablename__ = 'complex'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(Integer)

    analyses: Mapped[list['Analyse']] = relationship(secondary=AnalysesComplex, back_populates="complexes")
