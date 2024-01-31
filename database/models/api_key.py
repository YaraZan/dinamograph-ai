import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text
from sqlalchemy.orm import relationship

from database.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'))
    key = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='api_keys')