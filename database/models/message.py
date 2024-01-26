import uuid

from sqlalchemy import Column, Integer, String, UUID, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from database.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    is_ai_generated = Column(Boolean)
    created_at = Column(DateTime, default=func.now())

    chat = relationship('Chat', back_populates='messages')
