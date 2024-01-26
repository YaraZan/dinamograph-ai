from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Dnmh(Base):
    __tablename__ = "Dnmh"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Well_Id = Column(Integer)

    dnms = relationship('DnmPoint', back_populates='dnmh', lazy='dynamic')
