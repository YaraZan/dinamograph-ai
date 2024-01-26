import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, text
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())

    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='users')

    api_keys = relationship('ApiKey', back_populates='user')

    name = Column(String)
    email = Column(String)
    password = Column(String)
