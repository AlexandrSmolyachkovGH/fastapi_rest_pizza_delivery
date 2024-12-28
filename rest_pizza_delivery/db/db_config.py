from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv('DB_URI')
engine = create_engine(DB_URI, echo=True)

Base = declarative_base()
Session = sessionmaker()
