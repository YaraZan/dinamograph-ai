from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Marker(Base):
    __tablename__ = "markers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    url = Column(String)

    dnms = relationship('Dnm', back_populates='marker')
    ai_model_markers = relationship('AIMarker', back_populates='original_marker')
