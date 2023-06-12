from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from . import CONFIG

SQLALCHEMY_DATABASE_URL = CONFIG.SQLALCHEMY_DATABASE_URI

if CONFIG.STAGE == "TEST":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()