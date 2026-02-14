from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timezone
import os
import logging
import time
from sqlalchemy.exc import OperationalError


logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rce:rcepass@localhost:5432/rcedb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    code = Column(Text)
    status = Column(String)
    output = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)



def init_db():
    retries = 10
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database initialized successfully.")
            return
        except OperationalError as e:
            print("Database not ready, retrying...")
            retries -= 1
            time.sleep(2)

    raise Exception("Database could not be initialized.")
