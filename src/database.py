import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

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

from .users import models as user_models

while True:
    try:

        user_models.Base.metadata.create_all(bind=engine)
        break

    except OperationalError as e:

        print(f"WARNING:\tDB Connection failed due to {e}, retrying after 1 seconds")
        time.sleep(1)