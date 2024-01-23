from sqlalchemy import Column, Integer, String
from database.database import Base

class Marker(Base):
    __tablename__ = "markers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    url = Column(String)
