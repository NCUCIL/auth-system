from fastapi import FastAPI

from . import router, CONFIG, BaseConfig

app = FastAPI(**{**BaseConfig.__dict__, **CONFIG.__dict__})

app.include_router(router)