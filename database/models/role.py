import enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    # Create a relationship between Role and User
    users = relationship('User', back_populates='role')
