from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Dnm(Base):
    __tablename__ = "dnm"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dnmh_id = Column(Integer)
    marker_id = Column(Integer, ForeignKey('markers.id'))
    raw_url = Column(String)
    clear_url = Column(String)
    ready_url = Column(String)
    authored_id = Column(String)

    marker = relationship('Marker', back_populates='dnms')