from fastapi import FastAPI

from . import router, CONFIG, BaseConfig

app = FastAPI(**{**BaseConfig.__dict__, **CONFIG.__dict__})

@app.get('/')
async def root():
    return {"message": "Hello World"}

app.include_router(router)