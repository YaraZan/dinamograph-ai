import uuid

from sqlalchemy import Column, Integer, String, UUID, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())

    messages = relationship('Message', back_populates='chat')
