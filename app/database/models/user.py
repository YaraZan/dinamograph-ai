from sqlalchemy import Column, Integer, String
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(String)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    api_key = Column(String)
