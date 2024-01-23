from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(String)

    # Define the foreign key relationship
    role_id = Column(Integer, ForeignKey('roles.id'))

    # Create a relationship between User and Role
    role = relationship('Role', back_populates='users')

    name = Column(String)
    email = Column(String)
    password = Column(String)
    api_key = Column(String)
