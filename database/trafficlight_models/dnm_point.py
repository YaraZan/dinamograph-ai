from sqlalchemy import Column, Integer, String, SmallInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class DnmPoint(Base):
    __tablename__ = "Dnm"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Dnmh_Id = Column(Integer, ForeignKey('Dnmh.Id'))
    P = Column(SmallInteger)
    X = Column(Numeric)
    Y = Column(Numeric)

    dnmh = relationship('Dnmh', back_populates='dnms')
