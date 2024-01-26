import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text
from sqlalchemy.orm import relationship

from database.database import Base


class AIModel(Base):
    __tablename__ = 'ai_models'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ai_markers = relationship('AIMarker', back_populates='ai_model', cascade='all, delete-orphan')

