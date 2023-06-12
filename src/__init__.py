from dotenv import load_dotenv

load_dotenv()

import os
from .config import config, BaseConfig

CONFIG: BaseConfig = config.get(os.getenv("STAGE", "DEV"))


from .database import SessionLocal, engine
from .users import models as user_models

user_models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import APIRouter, status

router = APIRouter(
    prefix="/api/v1",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example":{
                        "detail": "Unauthorized",
                    },
                },
            },
        },
    }
)

from .users.router import router as user_router
from .auth.router import router as auth_router

router.include_router(user_router)
router.include_router(auth_router)