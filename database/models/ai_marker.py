import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text
from sqlalchemy.orm import relationship

from database.database import Base


class AIMarker(Base):
    __tablename__ = 'ai_markers'

    id = Column(Integer, primary_key=True)
    marker_id = Column(Integer, ForeignKey('markers.id'))
    ai_model_id = Column(Integer, ForeignKey('ai_models.id'))
    ai_model = relationship('AIModel', back_populates='ai_markers')
    original_marker = relationship('Marker', back_populates='ai_model_markers')
