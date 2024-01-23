from sqlalchemy import Column, Integer, String
from database.database import Base

class Dnm(Base):
    __tablename__ = "dnm"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dnmh_id = Column(Integer)
    marker_id = Column(Integer)
    raw_url = Column(String)
    clear_url = Column(String)
    ready_url = Column(String)
    authored_id = Column(String)
