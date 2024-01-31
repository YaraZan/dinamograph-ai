import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text, DateTime, func
from sqlalchemy.orm import relationship

from database.database import Base


class AIModel(Base):
    __tablename__ = 'ai_models'

    id = Column(Integer, primary_key=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    categories_num = Column(Integer)
    train_amount = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    ai_markers = relationship('AIMarker', back_populates='ai_model', cascade='all, delete-orphan')

