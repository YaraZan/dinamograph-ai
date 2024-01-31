import enum
import uuid

from sqlalchemy import Column, Integer, String, UUID, text
from sqlalchemy.orm import relationship

from database.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    name = Column(String)

    # Create a relationship between Role and User
    users = relationship('User', back_populates='role')
