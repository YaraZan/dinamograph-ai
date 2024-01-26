import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.environ.get('DATABASE_URL')
TRAFFICLIGHT_DATABASE_URL = os.environ.get('TRAFFICLIGHT_DATABASE_URL')

# Connect to the main database
engine1 = create_engine(DATABASE_URL)
Base.metadata.create_all(engine1)
MainSession = sessionmaker(bind=engine1)

# Connect to the TrafficLight database
engine2 = create_engine(TRAFFICLIGHT_DATABASE_URL)
Base.metadata.create_all(engine2)
TrafficLightSession = sessionmaker(bind=engine2)

