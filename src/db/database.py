from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import database_config

SQLALCHEMY_DATABASE_URL = database_config.get_db_url

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
